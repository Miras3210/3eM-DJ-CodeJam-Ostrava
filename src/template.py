import pyray as ray

width, height = 1600, 900

ray.set_trace_log_level(ray.TraceLogLevel.LOG_WARNING)
ray.init_window(width, height, "Project Name")

ray.set_target_fps(60)

while not ray.window_should_close():
    ray.begin_drawing()
    ray.clear_background(ray.WHITE)
    ray.end_drawing()
ray.close_window()