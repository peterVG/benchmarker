import sqlite3
import os
import logging
from datetime import datetime
import json
from pathlib import Path

# The central observability rule says stdout only.
logger = logging.getLogger(__name__)

# Fallback export file
FALLBACK_FILE = "data/fallback_results.json"

class DatabaseManager:
    def __init__(self, db_path="data/benchmarker.sqlite"):
        self.db_path = db_path
        # Ensure the directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    def _get_connection(self):
        # We use a timeout to handle concurrent writes if multiple harnesses run.
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        # WAL mode is better for concurrency
        conn.execute('PRAGMA journal_mode=WAL')
        return conn

    def initialize_schema(self):
        try:
            with self._get_connection() as conn:
                conn.execute("""
                CREATE TABLE IF NOT EXISTS runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_date TEXT NOT NULL,
                    hardware_profile TEXT NOT NULL,
                    model_name TEXT NOT NULL
                )
                """)
                
                conn.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER NOT NULL,
                    dataset_item_id TEXT,
                    latency_ms REAL,
                    time_to_first_token_ms REAL,
                    tokens_per_sec REAL,
                    vram_usage_mb REAL,
                    is_correct INTEGER,
                    FOREIGN KEY (run_id) REFERENCES runs (id)
                )
                """)
                logger.info("Database schema initialized successfully.")
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize database schema: {e}")
            raise

    def save_run(self, run_date, hardware_profile, model_name, metrics):
        """
        Save a run and its associated metrics to the database.
        If a permission error occurs, it writes to a fallback JSON file.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO runs (run_date, hardware_profile, model_name) VALUES (?, ?, ?)",
                    (run_date, hardware_profile, model_name)
                )
                run_id = cursor.lastrowid

                for metric in metrics:
                    cursor.execute(
                        """
                        INSERT INTO metrics 
                        (run_id, dataset_item_id, latency_ms, time_to_first_token_ms, tokens_per_sec, vram_usage_mb, is_correct) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            run_id,
                            metric.get("dataset_item_id"),
                            metric.get("latency_ms"),
                            metric.get("time_to_first_token_ms"),
                            metric.get("tokens_per_sec"),
                            metric.get("vram_usage_mb"),
                            metric.get("is_correct")
                        )
                    )
                conn.commit()
                logger.info(f"Successfully saved run {run_id} with {len(metrics)} metrics.")
                return run_id
        except sqlite3.OperationalError as e:
            if "readonly database" in str(e) or "attempt to write a readonly database" in str(e) or "permission denied" in str(e).lower():
                logger.warning(f"Database write permission error caught: {e}. Exporting to fallback JSON.")
                self._fallback_export(run_date, hardware_profile, model_name, metrics)
            else:
                logger.error(f"Database operational error: {e}")
                raise
        except sqlite3.Error as e:
            logger.error(f"Database error during save_run: {e}")
            raise

    def get_all_runs(self):
        """
        Retrieves all historical runs and calculates aggregated metrics for each run.
        """
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                # We need to join runs with metrics to get average latency and tokens_per_sec, and accuracy.
                cursor.execute("""
                SELECT 
                    r.id, r.run_date, r.hardware_profile, r.model_name,
                    COUNT(m.is_correct) as total_scored_items,
                    AVG(m.latency_ms) as avg_latency_ms,
                    AVG(m.tokens_per_sec) as avg_tokens_per_sec,
                    SUM(m.is_correct) as correct_items
                FROM runs r
                LEFT JOIN metrics m ON r.id = m.run_id
                GROUP BY r.id
                ORDER BY r.run_date DESC
                """)
                
                rows = cursor.fetchall()
                runs = []
                for row in rows:
                    total_items = row["total_scored_items"] or 0
                    correct_items = row["correct_items"] or 0
                    accuracy = (correct_items / total_items * 100) if total_items > 0 else 0
                    
                    runs.append({
                        "id": row["id"],
                        "run_date": row["run_date"],
                        "hardware_profile": row["hardware_profile"],
                        "model_name": row["model_name"],
                        "total_items": total_items,
                        "avg_latency_ms": row["avg_latency_ms"],
                        "avg_tokens_per_sec": row["avg_tokens_per_sec"],
                        "accuracy_percent": accuracy
                    })
                return runs
        except sqlite3.Error as e:
            logger.error(f"Failed to fetch runs: {e}")
            return []

    def _fallback_export(self, run_date, hardware_profile, model_name, metrics):
        Path(FALLBACK_FILE).parent.mkdir(parents=True, exist_ok=True)
        record = {
            "run_date": run_date,
            "hardware_profile": hardware_profile,
            "model_name": model_name,
            "metrics": metrics
        }
        
        existing_data = []
        if os.path.exists(FALLBACK_FILE):
            try:
                with open(FALLBACK_FILE, "r") as f:
                    existing_data = json.load(f)
            except json.JSONDecodeError:
                pass
                
        existing_data.append(record)
        
        with open(FALLBACK_FILE, "w") as f:
            json.dump(existing_data, f, indent=2)
        logger.info(f"Fallback export completed to {FALLBACK_FILE}.")
