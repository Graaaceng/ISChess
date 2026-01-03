from strategies.board_score import get_board_score


def time_percent_we_dominate(board, player_sequence, previous_score=0, total_play=0):

    # if int(player_sequence[0]) == 0:
    #     return (previous_score, total_play)

    current_score = get_board_score(board, player_sequence[1])
    score = previous_score
    if current_score > 0:
        score += 1

    return (score, total_play + 1)


class MetricsTracker:

    def __init__(self):
        self.domination_score = 0
        self.total_plays = 0
        self.total_time = 0.0
        self.move_times = []

    def update(self, board, player_sequence):
        """update les valeurs après un coup"""
        self.domination_score, self.total_plays = time_percent_we_dominate(
            board, player_sequence, self.domination_score, self.total_plays
        )

    def add_move_time(self, time_seconds):
        self.move_times.append(time_seconds)
        self.total_time += time_seconds

    def get_percentage(self):
        if self.total_plays == 0:
            return 0.0
        return (self.domination_score / self.total_plays) * 100

    def get_avg_time(self):
        if len(self.move_times) == 0:
            return 0.0
        return self.total_time / len(self.move_times)

    def get_summary(self):
        percentage = self.get_percentage()
        avg_time = self.get_avg_time()
        return f"Domination: {self.domination_score}/{self.total_plays} tours ({percentage:.1f}%) - Temps moy: {avg_time:.3f}s"

    def get_stats(self):
        return {
            "dom": self.domination_score,
            "plays": self.total_plays,
            "total_time": self.total_time,
            "avg_time": self.get_avg_time(),
        }
