from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from pubmed_pipeline.utils.log_config import get_logger

logger = get_logger(__name__)


class OutputWriter:
    """
    Small helper to persist LangGraph outputs (answer / summary / insights / etc.)
    under the `outputs/` folder so they can be inspected later.

    Directory layout (relative to project root):

    outputs/
      answers/
      summaries/
      insights/
    """

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        # project_root is two levels up from this file: pubmed_pipeline/output_writer/writer.py
        if base_dir is None:
            self.project_root = Path(__file__).resolve().parents[1]
        else:
            self.project_root = base_dir

        self.outputs_root = self.project_root / "outputs"
        self.answers_dir = self.outputs_root / "answers"
        self.summaries_dir = self.outputs_root / "summaries"
        self.insights_dir = self.outputs_root / "insights"

        # Ensure directories exist
        for d in [self.outputs_root, self.answers_dir, self.summaries_dir, self.insights_dir]:
            d.mkdir(parents=True, exist_ok=True)

        logger.info(f"OutputWriter initialized at: {self.outputs_root}")

    def _write_json(self, path: Path, payload: Dict[str, Any]) -> None:
        """Write a dict as pretty JSON."""
        with path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Wrote output file: {path}")

    def write_all(
        self,
        trace_id: str,
        answer: Optional[str],
        summary: Optional[str],
        insights: Optional[str],
        citations: Optional[List[str]] = None,
        debug: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Persist a single LangGraph run identified by trace_id.

        Each run writes:
        - answers/{trace_id}.json
        - summaries/{trace_id}.json
        - insights/{trace_id}.json
        """
        base_payload: Dict[str, Any] = {
            "trace_id": trace_id,
            "answer": answer,
            "summary": summary,
            "insights": insights,
            "citations": citations or [],
            "metadata": metadata or {},
            "debug": debug or {},
        }

        # Answer file
        self._write_json(self.answers_dir / f"{trace_id}.json", base_payload)

        # Summary-only file (still keeps context for debugging)
        summary_payload = dict(base_payload)
        self._write_json(self.summaries_dir / f"{trace_id}.json", summary_payload)

        # Insights-only file
        insights_payload = dict(base_payload)
        self._write_json(self.insights_dir / f"{trace_id}.json", insights_payload)

        logger.info(
            f"📦 OutputWriter.flush | trace_id={trace_id} | "
            f"answer_len={len(answer or '')} | summary_len={len(summary or '')}"
        )
