from abc import ABC
from typing import List, Dict

import pandas as pd

from server.analyzer.table_analyzer import TableAnalyzer, TableAnalyzerRegistry, LabelScore


class ToxicPairAnalyzer(TableAnalyzer, ABC):
    name = "toxic-pair"

    def analyze(self, table: str, columns: List[str], dataframes: List[pd.DataFrame]) -> Dict[str, LabelScore]:
        print(f">>>>>>>>>>Analyzing {table} with columns: {columns}")
        return {
            'toxic_pair': LabelScore(score=0.1, columns=columns)
        }


toxic_pair_analyzer = ToxicPairAnalyzer()
TableAnalyzerRegistry.add_table_analyser(toxic_pair_analyzer)
