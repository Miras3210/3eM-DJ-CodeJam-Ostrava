import pyray as ray

class Player:
    ...

def draw(width: int, height: int) -> None:
    ray.draw_rectangle(0,0,width, height, ray.WHITE) # BG color set

def main(width: int, height: int):
    ray.set_target_fps(60)
    while not ray.window_should_close():
        ray.begin_drawing()
        draw(width, height)
        ray.end_drawing()

if __name__ == "__main__":
    width, height = 1600, 900

    ray.set_trace_log_level(ray.TraceLogLevel.LOG_WARNING)
    ray.init_window(width, height, "Project Name")
    main(width, height)
    ray.close_window()