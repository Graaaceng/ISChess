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

        self.nodes_explored = []
        self.possible_moves = []
        self.material_history = []

    def update(self, board, player_sequence):
        """update les valeurs après un coup"""
        self.domination_score, self.total_plays = time_percent_we_dominate(
            board, player_sequence, self.domination_score, self.total_plays
        )

    def add_move_time(self, time_seconds):
        self.move_times.append(time_seconds)
        self.total_time += time_seconds

    def add_nodes_explored(self, nodes):
        self.nodes_explored.append(nodes)

    def add_possible_moves(self, count):
        self.possible_moves.append(count)

    def add_material_balance(self, material):
        self.material_history.append(material)

    def get_percentage(self):
        if self.total_plays == 0:
            return 0.0
        return (self.domination_score / self.total_plays) * 100

    def get_avg_time(self):
        if len(self.move_times) == 0:
            return 0.0
        return self.total_time / len(self.move_times)

    def get_avg_nodes(self):
        if len(self.nodes_explored) == 0:
            return 0
        return sum(self.nodes_explored) / len(self.nodes_explored)

    def get_avg_possible_moves(self):
        if len(self.possible_moves) == 0:
            return 0.0
        return sum(self.possible_moves) / len(self.possible_moves)

    def get_material_trend(self):
        if len(self.material_history) < 2:
            return 0
        return self.material_history[-1] - self.material_history[0]

    def get_summary(self):
        percentage = self.get_percentage()
        avg_time = self.get_avg_time()
        avg_nodes = self.get_avg_nodes()
        avg_pm = self.get_avg_possible_moves()
        return f"Domination: {self.domination_score}/{self.total_plays} tours ({percentage:.1f}%) - Temps moy: {avg_time:.3f}s - Nodes moy: {avg_nodes:.0f} - Moves moy: {avg_pm:.1f}"

    def get_stats(self):
        return {
            "dom": self.domination_score,
            "plays": self.total_plays,
            "total_time": self.total_time,
            "avg_time": self.get_avg_time(),
            "total_nodes": sum(self.nodes_explored) if self.nodes_explored else 0,
            "avg_nodes": self.get_avg_nodes(),
            "avg_possible_moves": self.get_avg_possible_moves(),
            "material_trend": self.get_material_trend(),
        }
