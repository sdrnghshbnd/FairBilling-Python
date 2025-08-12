class ResultsOutputter:
    @staticmethod
    def output(results: dict):
        for username, (session_count, total_time) in results.items():
            print(f"{username} {session_count} {total_time}")
