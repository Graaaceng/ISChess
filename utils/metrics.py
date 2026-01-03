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

    def update(self, board, player_sequence):
        """update les valeurs après un coup"""
        self.domination_score, self.total_plays = time_percent_we_dominate(
            board, player_sequence, self.domination_score, self.total_plays
        )

    def get_percentage(self):
        if self.total_plays == 0:
            return 0.0
        return (self.domination_score / self.total_plays) * 100

    def get_summary(self):
        percentage = self.get_percentage()
        return f"Domination: {self.domination_score}/{self.total_plays} tours ({percentage:.1f}%)"

    def get_stats(self):
        return {"dom": self.domination_score, "plays": self.total_plays}
