# def completion_percentage(watch_duration, total_duration):
#     if total_duration == 0:
#         return 0
#     return round((watch_duration / total_duration) * 100, 2)
def safe_text(value, default=""):
    return value if value else default
