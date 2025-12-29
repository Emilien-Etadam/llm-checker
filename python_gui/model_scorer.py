"""
Model Scoring Engine for LLM Checker
Scores models based on Quality, Speed, Fit, and Context
"""

from typing import Dict, List, Tuple
import math


class ModelScorer:
    """Scores LLM models based on hardware compatibility and use case"""

    def __init__(self):
        # Weight presets for different use cases
        self.weight_presets = {
            'general': {'Q': 0.40, 'S': 0.35, 'F': 0.15, 'C': 0.10},
            'coding': {'Q': 0.55, 'S': 0.20, 'F': 0.15, 'C': 0.10},
            'reasoning': {'Q': 0.60, 'S': 0.15, 'F': 0.10, 'C': 0.15},
            'chat': {'Q': 0.40, 'S': 0.40, 'F': 0.15, 'C': 0.05},
            'creative': {'Q': 0.50, 'S': 0.25, 'F': 0.15, 'C': 0.10},
            'fast': {'Q': 0.25, 'S': 0.55, 'F': 0.15, 'C': 0.05},
            'quality': {'Q': 0.65, 'S': 0.10, 'F': 0.15, 'C': 0.10}
        }

        # Model family quality rankings (base score 0-100)
        self.family_quality = {
            # Frontier models
            'qwen2.5': 95, 'qwen2': 90, 'llama3.3': 95, 'llama3.2': 92,
            'llama3.1': 90, 'llama3': 88, 'deepseek-v3': 96, 'deepseek-v2.5': 94,
            'deepseek-coder-v2': 92, 'deepseek-r1': 96, 'gemma2': 90, 'gemma': 82,
            'phi-4': 92, 'phi-3.5': 88, 'phi-3': 85, 'phi-2': 75,
            'mistral-large': 94, 'mistral': 85, 'mixtral': 88,
            'command-r': 90, 'command-r-plus': 93,

            # Coding specialists
            'qwen2.5-coder': 96, 'codellama': 82, 'starcoder2': 85,
            'deepseek-coder': 88, 'codegemma': 80, 'granite-code': 78,

            # Chat/instruct
            'yi': 85, 'yi-coder': 88, 'openchat': 78, 'neural-chat': 75,
            'zephyr': 80, 'openhermes': 82, 'nous-hermes': 82,
            'dolphin': 80, 'orca': 78,

            # Vision models
            'llava': 82, 'llava-llama3': 85, 'llava-phi3': 80,
            'bakllava': 78, 'moondream': 75,

            # Other notable models
            'solar': 82, 'falcon': 75, 'vicuna': 72, 'wizardlm': 78,
            'aya': 85, 'smollm': 70, 'tinyllama': 65
        }

        # Quantization quality penalties (subtracted from base)
        self.quant_penalties = {
            'FP16': 0, 'F16': 0, 'Q8_0': 2, 'Q6_K': 4, 'Q5_K_M': 6,
            'Q5_K_S': 7, 'Q5_0': 8, 'Q4_K_M': 10, 'Q4_K_S': 11,
            'Q4_0': 12, 'Q3_K_M': 16, 'Q3_K_S': 18, 'Q3_K_L': 15,
            'IQ4_XS': 11, 'IQ4_NL': 10, 'IQ3_XXS': 20, 'IQ3_XS': 18,
            'IQ3_S': 17, 'IQ2_XS': 25, 'IQ2_XXS': 28, 'Q2_K': 22, 'Q2_K_S': 24
        }

        # Task-specific bonuses
        self.task_bonuses = {
            'coding': {
                'qwen2.5-coder': 15, 'deepseek-coder': 12, 'deepseek-coder-v2': 15,
                'codellama': 10, 'starcoder2': 12, 'codegemma': 8,
                'yi-coder': 10, 'granite-code': 8
            },
            'reasoning': {
                'deepseek-r1': 15, 'qwen2.5': 10, 'llama3.3': 10,
                'phi-4': 12, 'command-r-plus': 10, 'mistral-large': 10
            },
            'chat': {
                'llama3.2': 10, 'mistral': 8, 'gemma2': 8,
                'openchat': 10, 'neural-chat': 8, 'dolphin': 8
            }
        }

    def score_model(self, model: Dict, hardware: Dict, use_case: str = 'general') -> Dict:
        """
        Score a single model variant

        Args:
            model: Dict with keys: name, params_b, size_gb, quantization, family, context_length
            hardware: Hardware detection result
            use_case: Use case for weighting

        Returns:
            Dict with scores and metadata
        """
        weights = self.weight_presets.get(use_case, self.weight_presets['general'])

        # Calculate individual scores
        q_score = self._quality_score(model, use_case)
        s_score = self._speed_score(model, hardware)
        f_score = self._fit_score(model, hardware)
        c_score = self._context_score(model)

        # Calculate weighted final score
        final_score = (
            q_score * weights['Q'] +
            s_score * weights['S'] +
            f_score * weights['F'] +
            c_score * weights['C']
        )

        return {
            'model': model,
            'scores': {
                'quality': round(q_score, 1),
                'speed': round(s_score, 1),
                'fit': round(f_score, 1),
                'context': round(c_score, 1),
                'final': round(final_score, 1)
            },
            'estimated_tps': self._estimate_tps(model, hardware),
            'will_fit': self._will_fit(model, hardware)
        }

    def _quality_score(self, model: Dict, use_case: str) -> float:
        """Calculate quality score (0-100)"""
        family = model.get('family', '').lower()
        params_b = model.get('params_b', 7)
        quantization = model.get('quantization', 'Q4_K_M')

        # Base score from family
        base_score = self.family_quality.get(family, 70)

        # Parameter bonus (diminishing returns)
        param_bonus = min(15, math.log2(params_b + 1) * 3)

        # Quantization penalty
        quant_penalty = self.quant_penalties.get(quantization, 10)

        # Task-specific bonus
        task_bonus = 0
        if use_case in self.task_bonuses:
            task_bonus = self.task_bonuses[use_case].get(family, 0)

        score = base_score + param_bonus - quant_penalty + task_bonus
        return max(0, min(100, score))

    def _speed_score(self, model: Dict, hardware: Dict) -> float:
        """Calculate speed score based on estimated tokens/second"""
        tps = self._estimate_tps(model, hardware)

        # Score based on TPS ranges
        # 100+ tps = 100 score, 1 tps = 0 score, log scale
        if tps <= 0:
            return 0

        # Logarithmic scoring: 1 tps = 0, 10 tps = 50, 100 tps = 100
        score = (math.log10(tps) / math.log10(100)) * 100
        return max(0, min(100, score))

    def _fit_score(self, model: Dict, hardware: Dict) -> float:
        """Calculate how well the model fits in memory"""
        size_gb = model.get('size_gb', 0)
        max_size = hardware['summary']['max_model_size_gb']

        if size_gb <= 0 or max_size <= 0:
            return 0

        utilization = size_gb / max_size

        # Perfect fit: 70-80% utilization = 100 score
        # Under 50%: proportional penalty
        # Over 90%: steep penalty
        # Over 100%: 0 score
        if utilization > 1.0:
            return 0
        elif utilization > 0.9:
            return (1.0 - utilization) * 1000  # Steep drop
        elif 0.7 <= utilization <= 0.85:
            return 100  # Perfect range
        elif utilization < 0.7:
            # Linear from 0% (score=50) to 70% (score=100)
            return 50 + (utilization / 0.7) * 50
        else:  # 0.85 < utilization <= 0.9
            # Linear from 85% (score=100) to 90% (score=80)
            return 100 - ((utilization - 0.85) / 0.05) * 20

    def _context_score(self, model: Dict) -> float:
        """Score based on context length"""
        context = model.get('context_length', 8192)

        # Logarithmic scoring: 2k = 30, 8k = 70, 32k = 90, 128k = 100
        if context <= 0:
            return 30

        score = 30 + (math.log2(context / 2048) * 20)
        return max(30, min(100, score))

    def _estimate_tps(self, model: Dict, hardware: Dict) -> float:
        """Estimate tokens per second"""
        params_b = model.get('params_b', 7)
        quantization = model.get('quantization', 'Q4_K_M')
        speed_coef = hardware['summary']['speed_coefficient']

        # Base formula
        base_tps = speed_coef / (params_b ** 0.5)

        # Quantization multipliers
        quant_multipliers = {
            'FP16': 0.6, 'Q8_0': 0.85, 'Q6_K': 1.0, 'Q5_K_M': 1.1,
            'Q4_K_M': 1.3, 'Q4_0': 1.35, 'Q3_K_M': 1.5, 'Q2_K': 1.7
        }

        multiplier = quant_multipliers.get(quantization, 1.0)
        return round(base_tps * multiplier, 1)

    def _will_fit(self, model: Dict, hardware: Dict) -> bool:
        """Check if model will fit in memory"""
        size_gb = model.get('size_gb', 0)
        max_size = hardware['summary']['max_model_size_gb']
        return size_gb <= max_size

    def score_models(self, models: List[Dict], hardware: Dict, use_case: str = 'general',
                     limit: int = 10) -> List[Dict]:
        """
        Score multiple models and return top recommendations

        Args:
            models: List of model dicts
            hardware: Hardware detection result
            use_case: Use case for scoring
            limit: Max number of results

        Returns:
            List of scored models sorted by final score
        """
        scored = []

        for model in models:
            try:
                score_result = self.score_model(model, hardware, use_case)
                if score_result['will_fit']:  # Only include models that fit
                    scored.append(score_result)
            except Exception as e:
                # Skip models that fail to score
                continue

        # Sort by final score descending
        scored.sort(key=lambda x: x['scores']['final'], reverse=True)

        return scored[:limit]

    def categorize_scores(self, scored_models: List[Dict]) -> Dict:
        """Categorize models by different metrics"""
        if not scored_models:
            return {
                'best_overall': None,
                'highest_quality': None,
                'fastest': None,
                'best_fit': None
            }

        return {
            'best_overall': max(scored_models, key=lambda x: x['scores']['final']),
            'highest_quality': max(scored_models, key=lambda x: x['scores']['quality']),
            'fastest': max(scored_models, key=lambda x: x['scores']['speed']),
            'best_fit': max(scored_models, key=lambda x: x['scores']['fit'])
        }
