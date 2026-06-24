def formatTime(milliseconds):

    totalSeconds = milliseconds // 1000

    hours = totalSeconds // 3600
    minutes = (totalSeconds % 3600) // 60
    seconds = totalSeconds % 60

    if hours > 0:
        return f'{hours:02}:{minutes:02}:{seconds:02}'

    return f'{minutes:02}:{seconds:02}'