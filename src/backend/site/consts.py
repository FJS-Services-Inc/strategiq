from collections import defaultdict
from typing import Any, Final

ANALYZING_MESSAGE: Final = "Analyzing..."
ANALYSIS_COMPLETE_MESSAGE = "Analysis complete!"

running_tasks = set()
status_store: dict[str, list] = defaultdict(list)
result_store: dict[str, Any] = {}
# Track last message count seen by each session for incremental updates
last_message_index: dict[str, int] = defaultdict(int)
