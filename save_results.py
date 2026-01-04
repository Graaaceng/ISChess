import csv
import os


class ResultSaver:
    def __init__(self):
        self.filename = "results.csv"
        self.results = []
        self.load_existing()

    def load_existing(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    self.results = list(reader)
                    for r in self.results:
                        r["game"] = int(r["game"])
            except:
                self.results = []

    def add_result(
        self, winner, white_bot, black_bot, white_stats, black_stats, total_turns
    ):
        result = {
            "game": len(self.results) + 1,
            "winner": winner,
            "white_bot": white_bot,
            "black_bot": black_bot,
            "total_turns": total_turns,
            "metric": "time_percent_we_dominate",
            "white_dom": white_stats["dom"],
            "white_plays": white_stats["plays"],
            "white_pct": (
                (white_stats["dom"] / white_stats["plays"] * 100)
                if white_stats["plays"] > 0
                else 0
            ),
            "black_dom": black_stats["dom"],
            "black_plays": black_stats["plays"],
            "black_pct": (
                (black_stats["dom"] / black_stats["plays"] * 100)
                if black_stats["plays"] > 0
                else 0
            ),
            "white_avg_time": white_stats["avg_time"],
            "white_total_time": white_stats["total_time"],
            "black_avg_time": black_stats["avg_time"],
            "black_total_time": black_stats["total_time"],
        }
        self.results.append(result)
        self.save()

    def save(self):
        if not self.results:
            return

        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
            writer.writeheader()
            writer.writerows(self.results)

        print(f"Resultat sauvegardé)")

    def save_game_result(self, winner_color, players):

        white_player = next((p for p in players if p.color == "w"), None)
        black_player = next((p for p in players if p.color == "b"), None)

        if not white_player or not black_player:
            return

        white_bot = white_player.widget.playerBot.currentText()
        black_bot = black_player.widget.playerBot.currentText()
        white_stats = white_player.metrics.get_stats()
        black_stats = black_player.metrics.get_stats()
        total_turns = white_stats["plays"] + black_stats["plays"]

        self.add_result(
            winner_color, white_bot, black_bot, white_stats, black_stats, total_turns
        )
