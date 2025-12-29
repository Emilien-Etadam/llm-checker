"""
Hardware Detection Module for LLM Checker GUI
Detects CPU, GPU (NVIDIA, AMD, Intel), and memory to recommend optimal LLM models
"""

import platform
import subprocess
import re
import psutil
from typing import Dict, Optional, List


class HardwareDetector:
    """Detects system hardware and calculates optimal settings for LLM models"""

    def __init__(self):
        self.cache = None

    def detect(self) -> Dict:
        """Main detection method - returns comprehensive hardware info"""
        if self.cache:
            return self.cache

        result = {
            'cpu': self._detect_cpu(),
            'gpu': self._detect_gpu(),
            'memory': self._detect_memory(),
            'platform': self._detect_platform()
        }

        # Determine best backend and calculate scores
        result['backend'] = self._select_backend(result)
        result['summary'] = self._build_summary(result)
        result['tier'] = self._get_hardware_tier(result)

        self.cache = result
        return result

    def _detect_cpu(self) -> Dict:
        """Detect CPU information"""
        try:
            cpu_info = {
                'brand': platform.processor() or 'Unknown CPU',
                'cores_physical': psutil.cpu_count(logical=False) or 1,
                'cores_logical': psutil.cpu_count(logical=True) or 1,
                'frequency_mhz': 0
            }

            # Get CPU frequency
            freq = psutil.cpu_freq()
            if freq:
                cpu_info['frequency_mhz'] = freq.max or freq.current or 0

            # Detect SIMD capabilities
            cpu_info['simd'] = self._detect_simd()

            # Calculate CPU speed coefficient (rough estimation)
            cpu_info['speed_coefficient'] = self._estimate_cpu_speed(cpu_info)

            return cpu_info
        except Exception as e:
            return {
                'brand': 'Unknown',
                'cores_physical': 1,
                'cores_logical': 1,
                'frequency_mhz': 0,
                'simd': 'Unknown',
                'speed_coefficient': 10
            }

    def _detect_simd(self) -> str:
        """Detect SIMD instruction set"""
        system = platform.system()
        arch = platform.machine().lower()

        if 'arm' in arch or 'aarch64' in arch:
            return 'NEON'

        if system == 'Windows':
            # On Windows, assume AVX2 for modern CPUs
            return 'AVX2'

        try:
            if system == 'Linux':
                with open('/proc/cpuinfo', 'r') as f:
                    cpuinfo = f.read()
                    if 'avx512' in cpuinfo:
                        return 'AVX-512'
                    elif 'avx2' in cpuinfo:
                        return 'AVX2'
                    elif 'avx' in cpuinfo:
                        return 'AVX'
                    elif 'sse4' in cpuinfo:
                        return 'SSE4'
        except:
            pass

        return 'Unknown'

    def _estimate_cpu_speed(self, cpu_info: Dict) -> float:
        """Estimate CPU inference speed coefficient"""
        base_speed = 10.0

        # Bonus for more cores
        cores = cpu_info['cores_physical']
        if cores >= 16:
            base_speed += 20
        elif cores >= 12:
            base_speed += 15
        elif cores >= 8:
            base_speed += 10
        elif cores >= 6:
            base_speed += 5

        # SIMD bonuses
        simd = cpu_info.get('simd', '')
        if 'AVX-512' in simd:
            base_speed += 30
        elif 'AVX2' in simd:
            base_speed += 20
        elif 'AVX' in simd:
            base_speed += 10
        elif 'NEON' in simd:
            base_speed += 15

        return base_speed

    def _detect_gpu(self) -> Dict:
        """Detect GPU information (NVIDIA, AMD, Intel)"""
        gpu_info = {
            'nvidia': None,
            'amd': None,
            'intel': None,
            'has_gpu': False
        }

        # Try NVIDIA first
        nvidia = self._detect_nvidia_gpu()
        if nvidia:
            gpu_info['nvidia'] = nvidia
            gpu_info['has_gpu'] = True

        # Try AMD
        amd = self._detect_amd_gpu()
        if amd:
            gpu_info['amd'] = amd
            gpu_info['has_gpu'] = True

        # Try Intel
        intel = self._detect_intel_gpu()
        if intel:
            gpu_info['intel'] = intel
            gpu_info['has_gpu'] = True

        return gpu_info

    def _detect_nvidia_gpu(self) -> Optional[Dict]:
        """Detect NVIDIA GPU using nvidia-smi"""
        try:
            # Try nvidia-smi command
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader,nounits'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                gpus = []
                total_vram = 0

                for line in lines:
                    parts = line.split(',')
                    if len(parts) >= 2:
                        name = parts[0].strip()
                        vram_mb = float(parts[1].strip())
                        vram_gb = vram_mb / 1024
                        gpus.append({'name': name, 'vram_gb': vram_gb})
                        total_vram += vram_gb

                if gpus:
                    return {
                        'available': True,
                        'gpus': gpus,
                        'total_vram': total_vram,
                        'count': len(gpus),
                        'speed_coefficient': self._nvidia_speed_coefficient(gpus[0]['name'])
                    }
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        return None

    def _nvidia_speed_coefficient(self, gpu_name: str) -> float:
        """Estimate NVIDIA GPU speed based on model name"""
        name_lower = gpu_name.lower()

        # High-end data center
        if 'h100' in name_lower:
            return 500
        if 'a100' in name_lower:
            return 400
        if 'v100' in name_lower:
            return 300

        # RTX 40 series
        if '4090' in name_lower:
            return 350
        if '4080' in name_lower:
            return 280
        if '4070' in name_lower:
            return 220
        if '4060' in name_lower:
            return 160

        # RTX 30 series
        if '3090' in name_lower:
            return 250
        if '3080' in name_lower:
            return 220
        if '3070' in name_lower:
            return 180
        if '3060' in name_lower:
            return 140

        # RTX 20 series
        if '2080' in name_lower or '2070' in name_lower:
            return 150
        if '2060' in name_lower:
            return 120

        # GTX 16 series
        if '1660' in name_lower or '1650' in name_lower:
            return 80

        # Default for unknown NVIDIA
        return 100

    def _detect_amd_gpu(self) -> Optional[Dict]:
        """Detect AMD GPU using rocm-smi or fallback methods"""
        try:
            # Try rocm-smi
            result = subprocess.run(
                ['rocm-smi', '--showproductname'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                # Parse output for GPU info
                output = result.stdout
                if 'GPU' in output:
                    # Simplified detection - just know we have AMD
                    return {
                        'available': True,
                        'gpus': [{'name': 'AMD GPU', 'vram_gb': 8}],  # Estimate
                        'total_vram': 8,
                        'count': 1,
                        'speed_coefficient': 150
                    }
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        return None

    def _detect_intel_gpu(self) -> Optional[Dict]:
        """Detect Intel GPU (Arc, Iris, UHD)"""
        # This is harder to detect reliably on Windows without specific tools
        # For now, return None - CPU path will be used
        return None

    def _detect_memory(self) -> Dict:
        """Detect system memory"""
        mem = psutil.virtual_memory()
        return {
            'total_gb': mem.total / (1024 ** 3),
            'available_gb': mem.available / (1024 ** 3),
            'percent_used': mem.percent
        }

    def _detect_platform(self) -> Dict:
        """Detect OS and platform info"""
        return {
            'system': platform.system(),
            'release': platform.release(),
            'machine': platform.machine(),
            'python_version': platform.python_version()
        }

    def _select_backend(self, hw: Dict) -> Dict:
        """Select the best backend for LLM inference"""
        gpu = hw['gpu']

        # Priority: NVIDIA > AMD > Intel > CPU
        if gpu['nvidia']:
            return {
                'type': 'cuda',
                'name': 'NVIDIA CUDA',
                'gpu_name': gpu['nvidia']['gpus'][0]['name'],
                'vram_gb': gpu['nvidia']['total_vram'],
                'speed': gpu['nvidia']['speed_coefficient']
            }

        if gpu['amd']:
            return {
                'type': 'rocm',
                'name': 'AMD ROCm',
                'gpu_name': gpu['amd']['gpus'][0]['name'],
                'vram_gb': gpu['amd']['total_vram'],
                'speed': gpu['amd']['speed_coefficient']
            }

        if gpu['intel']:
            return {
                'type': 'intel',
                'name': 'Intel Arc',
                'gpu_name': gpu['intel']['gpus'][0]['name'],
                'vram_gb': gpu['intel']['total_vram'],
                'speed': gpu['intel']['speed_coefficient']
            }

        # Fallback to CPU
        return {
            'type': 'cpu',
            'name': 'CPU',
            'gpu_name': None,
            'vram_gb': 0,
            'speed': hw['cpu']['speed_coefficient']
        }

    def _build_summary(self, hw: Dict) -> Dict:
        """Build a summary of hardware capabilities"""
        backend = hw['backend']
        memory = hw['memory']

        # Calculate effective memory for LLM loading
        if backend['type'] in ['cuda', 'rocm', 'intel']:
            # GPU: use VRAM with 2GB headroom
            effective_memory = max(0, backend['vram_gb'] - 2)
        else:
            # CPU: use 70% of system RAM
            effective_memory = memory['total_gb'] * 0.7

        return {
            'backend_type': backend['type'],
            'backend_name': backend['name'],
            'max_model_size_gb': round(effective_memory, 1),
            'speed_coefficient': backend['speed'],
            'total_ram_gb': round(memory['total_gb'], 1),
            'description': self._get_description(hw)
        }

    def _get_description(self, hw: Dict) -> str:
        """Get human-readable hardware description"""
        backend = hw['backend']
        cpu = hw['cpu']
        mem = hw['memory']

        if backend['type'] in ['cuda', 'rocm', 'intel']:
            return f"{backend['gpu_name']} ({backend['vram_gb']:.0f}GB VRAM) + {cpu['cores_physical']} cores"
        else:
            return f"{cpu['brand']} ({cpu['cores_physical']} cores, {mem['total_gb']:.0f}GB RAM)"

    def _get_hardware_tier(self, hw: Dict) -> str:
        """Classify hardware into tiers"""
        summary = hw['summary']
        max_size = summary['max_model_size_gb']
        speed = summary['speed_coefficient']

        if max_size >= 80 and speed >= 300:
            return 'ULTRA HIGH'
        if max_size >= 48 and speed >= 200:
            return 'VERY HIGH'
        if max_size >= 24 and speed >= 150:
            return 'HIGH'
        if max_size >= 16 and speed >= 100:
            return 'MEDIUM HIGH'
        if max_size >= 12 and speed >= 80:
            return 'MEDIUM'
        if max_size >= 8 and speed >= 50:
            return 'MEDIUM LOW'
        if max_size >= 6 and speed >= 30:
            return 'LOW'
        return 'ULTRA LOW'

    def estimate_tokens_per_second(self, params_b: float, quantization: str = 'Q4_K_M') -> float:
        """Estimate tokens/second for a given model size"""
        if not self.cache:
            self.detect()

        speed_coef = self.cache['summary']['speed_coefficient']

        # Base formula: speed decreases with model size
        # Rough approximation based on real-world benchmarks
        base_tps = speed_coef / (params_b ** 0.5)

        # Quantization adjustments
        quant_multipliers = {
            'FP16': 0.6,
            'Q8_0': 0.85,
            'Q6_K': 1.0,
            'Q5_K_M': 1.1,
            'Q4_K_M': 1.3,
            'Q4_0': 1.35,
            'Q3_K_M': 1.5,
            'Q2_K': 1.7
        }

        multiplier = quant_multipliers.get(quantization, 1.0)
        return round(base_tps * multiplier, 1)

    def will_model_fit(self, size_gb: float) -> bool:
        """Check if a model will fit in available memory"""
        if not self.cache:
            self.detect()

        return size_gb <= self.cache['summary']['max_model_size_gb']

    def get_recommended_quantizations(self, params_b: float) -> List[str]:
        """Get recommended quantization levels for a model"""
        if not self.cache:
            self.detect()

        max_size = self.cache['summary']['max_model_size_gb']
        recommendations = []

        # Size estimates for different quantizations
        quant_sizes = {
            'FP16': params_b * 2.0,
            'Q8_0': params_b * 1.1,
            'Q6_K': params_b * 0.85,
            'Q5_K_M': params_b * 0.75,
            'Q4_K_M': params_b * 0.65,
            'Q4_0': params_b * 0.55,
            'Q3_K_M': params_b * 0.45,
            'Q2_K': params_b * 0.35
        }

        # Quality order
        quality_order = ['FP16', 'Q8_0', 'Q6_K', 'Q5_K_M', 'Q4_K_M', 'Q4_0', 'Q3_K_M', 'Q2_K']

        for quant in quality_order:
            if quant_sizes[quant] <= max_size:
                recommendations.append(quant)

        return recommendations[:3] if recommendations else ['Q4_K_M']
