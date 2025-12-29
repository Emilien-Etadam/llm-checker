"""
Ollama Model Synchronization Module
Fetches latest models from Ollama website and caches them locally
"""

import requests
import re
import sqlite3
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class OllamaSync:
    """Synchronizes model database with Ollama website"""

    def __init__(self, cache_dir: str = None):
        if cache_dir is None:
            # Use user's AppData folder on Windows
            cache_dir = Path.home() / ".llm_checker"

        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.db_path = self.cache_dir / "models_cache.db"
        self.base_url = "https://ollama.com"

        # Request settings
        self.timeout = 15
        self.max_retries = 3
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }

        self._init_database()

    def _init_database(self):
        """Initialize SQLite database for caching"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Models table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS models (
                id TEXT PRIMARY KEY,
                name TEXT,
                family TEXT,
                params_b REAL,
                size_gb REAL,
                quantization TEXT,
                context_length INTEGER,
                pulls INTEGER,
                last_updated TEXT,
                cached_at TEXT
            )
        ''')

        # Sync metadata table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sync_meta (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def get_last_sync_time(self) -> Optional[datetime]:
        """Get the timestamp of last successful sync"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT value FROM sync_meta WHERE key = ?', ('last_sync',))
        row = cursor.fetchone()
        conn.close()

        if row:
            return datetime.fromisoformat(row[0])
        return None

    def set_last_sync_time(self):
        """Update last sync timestamp"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        now = datetime.now().isoformat()
        cursor.execute('''
            INSERT OR REPLACE INTO sync_meta (key, value, updated_at)
            VALUES (?, ?, ?)
        ''', ('last_sync', now, now))

        conn.commit()
        conn.close()

    def fetch_model_list(self) -> List[str]:
        """Fetch list of model IDs from Ollama library page"""
        url = f"{self.base_url}/library"

        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
                response.raise_for_status()

                html = response.text

                # Extract model IDs from library links
                # Pattern: href="/library/model-name"
                pattern = r'href="/library/([^"/?#]+)"'
                matches = re.findall(pattern, html)

                # Deduplicate and filter
                model_ids = list(set([m.lower() for m in matches if m and not m.startswith('tags')]))

                return model_ids

            except requests.RequestException as e:
                if attempt < self.max_retries - 1:
                    time.sleep((attempt + 1) * 2)  # Exponential backoff
                    continue
                else:
                    raise Exception(f"Failed to fetch model list: {str(e)}")

    def fetch_model_tags(self, model_id: str) -> List[Dict]:
        """Fetch all tags/variants for a specific model"""
        url = f"{self.base_url}/library/{model_id}/tags"

        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()

            html = response.text
            variants = []

            # Pattern 1: Extract tag:variant with size
            # Example: "llama3.1:8b    4.9GB"
            pattern1 = rf'({model_id}:[\w\d\.\-]+)\s+[\n\r\s]+([\d\.]+)\s*(GB|MB)'
            matches = re.finditer(pattern1, html, re.IGNORECASE)

            seen_tags = set()
            for match in matches:
                tag = match.group(1)
                size_num = float(match.group(2))
                size_unit = match.group(3).upper()

                # Convert to GB
                size_gb = size_num if size_unit == 'GB' else size_num / 1024

                if tag not in seen_tags:
                    seen_tags.add(tag)
                    variant = self._parse_variant(model_id, tag, size_gb)
                    if variant:
                        variants.append(variant)

            # Pattern 2: Find all mentions of tags (even without size)
            pattern2 = rf'{model_id}:([\w\d\.\-]+)'
            matches = re.finditer(pattern2, html, re.IGNORECASE)

            for match in matches:
                tag = f"{model_id}:{match.group(1)}"
                if tag not in seen_tags:
                    seen_tags.add(tag)
                    variant = self._parse_variant(model_id, tag, None)
                    if variant:
                        variants.append(variant)

            return variants

        except requests.RequestException:
            # If we can't fetch tags, return empty list
            return []

    def _parse_variant(self, model_id: str, tag: str, size_gb: Optional[float]) -> Optional[Dict]:
        """Parse a model variant tag into structured data"""
        # Extract components from tag
        # Format: model-name:size-variant-quantization
        # Example: llama3.1:8b-instruct-q4_k_m

        try:
            parts = tag.split(':')
            if len(parts) != 2:
                return None

            base_name = parts[0]
            variant_str = parts[1]

            # Extract parameter size (1b, 7b, 70b, etc.)
            params_match = re.search(r'(\d+(?:\.\d+)?)\s*b', variant_str, re.IGNORECASE)
            params_b = float(params_match.group(1)) if params_match else 7.0  # Default

            # Extract quantization
            quantization = 'Q4_K_M'  # Default
            quant_patterns = [
                r'q(\d+)_k_m', r'q(\d+)_k_s', r'q(\d+)_k_l', r'q(\d+)_k',
                r'q(\d+)_0', r'fp16', r'f16', r'iq(\d+)_\w+'
            ]

            for pattern in quant_patterns:
                match = re.search(pattern, variant_str, re.IGNORECASE)
                if match:
                    quantization = match.group(0).upper()
                    break

            # Estimate size if not provided
            if size_gb is None:
                size_gb = self._estimate_size(params_b, quantization)

            # Determine model family
            family = self._extract_family(base_name)

            # Context length (default based on family)
            context_length = self._get_default_context(family)

            return {
                'id': tag,
                'name': tag,
                'family': family,
                'params_b': params_b,
                'size_gb': round(size_gb, 1),
                'quantization': quantization,
                'context_length': context_length,
                'pulls': 0,
                'last_updated': datetime.now().isoformat()
            }

        except Exception:
            return None

    def _estimate_size(self, params_b: float, quantization: str) -> float:
        """Estimate model size based on parameters and quantization"""
        # Size multipliers for different quantizations
        multipliers = {
            'FP16': 2.0, 'F16': 2.0,
            'Q8_0': 1.1, 'Q6_K': 0.85, 'Q5_K_M': 0.75,
            'Q4_K_M': 0.65, 'Q4_0': 0.55, 'Q3_K_M': 0.45,
            'Q2_K': 0.35
        }

        multiplier = multipliers.get(quantization, 0.65)  # Default to Q4_K_M
        return params_b * multiplier

    def _extract_family(self, model_name: str) -> str:
        """Extract model family from model name"""
        # Common patterns
        families = {
            'qwen2.5-coder': r'qwen2\.5-coder',
            'qwen2.5': r'qwen2\.5',
            'qwen2': r'qwen2',
            'llama3.3': r'llama3\.3',
            'llama3.2': r'llama3\.2',
            'llama3.1': r'llama3\.1',
            'llama3': r'llama3',
            'deepseek-r1': r'deepseek-r1',
            'deepseek-coder-v2': r'deepseek-coder-v2',
            'deepseek-coder': r'deepseek-coder',
            'phi4': r'phi-?4',
            'phi-3.5': r'phi-?3\.5',
            'phi-3': r'phi-?3',
            'gemma2': r'gemma2',
            'mistral': r'mistral',
            'mixtral': r'mixtral',
            'codellama': r'codellama',
        }

        for family, pattern in families.items():
            if re.search(pattern, model_name, re.IGNORECASE):
                return family

        # Default: use base name
        return model_name.split('-')[0].lower()

    def _get_default_context(self, family: str) -> int:
        """Get default context length for a model family"""
        context_map = {
            'qwen2.5-coder': 32768,
            'qwen2.5': 128000,
            'llama3.3': 128000,
            'llama3.2': 131072,
            'llama3.1': 131072,
            'deepseek-r1': 32768,
            'deepseek-coder-v2': 131072,
            'phi4': 16384,
            'gemma2': 8192,
            'mistral': 32768,
        }

        return context_map.get(family, 8192)  # Default 8K

    def sync_models(self, on_progress=None) -> int:
        """
        Sync models from Ollama website
        Returns number of models synced
        """
        if on_progress:
            on_progress("Fetching model list from ollama.com...")

        # Fetch list of model IDs
        model_ids = self.fetch_model_list()

        if on_progress:
            on_progress(f"Found {len(model_ids)} models, fetching variants...")

        # Fetch variants for each model
        all_variants = []
        for i, model_id in enumerate(model_ids):
            if on_progress and i % 10 == 0:
                on_progress(f"Processing {i+1}/{len(model_ids)}: {model_id}")

            variants = self.fetch_model_tags(model_id)
            all_variants.extend(variants)

            # Rate limiting
            time.sleep(0.2)

        # Save to database
        if on_progress:
            on_progress(f"Saving {len(all_variants)} model variants to cache...")

        self._save_to_cache(all_variants)
        self.set_last_sync_time()

        if on_progress:
            on_progress(f"✅ Sync complete! {len(all_variants)} models cached")

        return len(all_variants)

    def _save_to_cache(self, variants: List[Dict]):
        """Save model variants to SQLite cache"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Clear existing data
        cursor.execute('DELETE FROM models')

        # Insert new data
        now = datetime.now().isoformat()
        for variant in variants:
            cursor.execute('''
                INSERT OR REPLACE INTO models
                (id, name, family, params_b, size_gb, quantization, context_length, pulls, last_updated, cached_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                variant['id'],
                variant['name'],
                variant['family'],
                variant['params_b'],
                variant['size_gb'],
                variant['quantization'],
                variant['context_length'],
                variant.get('pulls', 0),
                variant.get('last_updated', now),
                now
            ))

        conn.commit()
        conn.close()

    def get_cached_models(self) -> List[Dict]:
        """Get models from local cache"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, name, family, params_b, size_gb, quantization, context_length, pulls, last_updated
            FROM models
            ORDER BY pulls DESC, params_b ASC
        ''')

        rows = cursor.fetchall()
        conn.close()

        models = []
        for row in rows:
            models.append({
                'id': row[0],
                'name': row[1],
                'family': row[2],
                'params_b': row[3],
                'size_gb': row[4],
                'quantization': row[5],
                'context_length': row[6],
                'pulls': row[7],
                'last_updated': row[8]
            })

        return models

    def get_models(self, force_sync: bool = False) -> List[Dict]:
        """
        Get models - try online first, fallback to cache

        Args:
            force_sync: If True, always sync from online

        Returns:
            List of model dictionaries
        """
        # If force sync or no cache, try to sync
        if force_sync or self.get_last_sync_time() is None:
            try:
                self.sync_models()
                return self.get_cached_models()
            except Exception:
                # If sync fails, fall back to cache
                pass

        # Try to get from cache
        cached = self.get_cached_models()
        if cached:
            return cached

        # If no cache, try to sync one more time
        try:
            self.sync_models()
            return self.get_cached_models()
        except Exception:
            # If everything fails, return empty list
            # The GUI will fall back to hardcoded database
            return []

    def is_cache_fresh(self, max_age_hours: int = 24) -> bool:
        """Check if cache is fresh enough"""
        last_sync = self.get_last_sync_time()
        if not last_sync:
            return False

        age = datetime.now() - last_sync
        return age.total_seconds() < (max_age_hours * 3600)
