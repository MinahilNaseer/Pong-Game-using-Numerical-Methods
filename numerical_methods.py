import numpy as np
def rk4_predict_position(ball, ball_dx, ball_dy, time_step):
    x, y = ball.x, ball.y
    vx, vy = ball_dx, ball_dy

    k1_x = vx * time_step
    k1_y = vy * time_step
    k2_x = (vx + k1_x / 2) * time_step
    k2_y = (vy + k1_y / 2) * time_step
    k3_x = (vx + k2_x / 2) * time_step
    k3_y = (vy + k2_y / 2) * time_step
    k4_x = (vx + k3_x) * time_step
    k4_y = (vy + k3_y) * time_step

    predicted_x = x + (k1_x + 2 * k2_x + 2 * k3_x + k4_x) / 6
    predicted_y = y + (k1_y + 2 * k2_y + 2 * k3_y + k4_y) / 6

    return predicted_x, predicted_y

def euler_predict_position(ball, ball_dx, ball_dy, time_step):
    return ball.x + ball_dx * time_step, ball.y + ball_dy * time_step

def bisection_method_for_collision(ball, target_x,ball_dx, ball_dy, tolerance=1e-2):
    lower_bound = 0
    upper_bound = 1
    predicted_time = None

    while upper_bound - lower_bound > tolerance:
        mid_time = (upper_bound + lower_bound) / 2
        predicted_x, _ = euler_predict_position(ball, ball_dx, ball_dy, mid_time)

        if predicted_x < target_x:
            lower_bound = mid_time
        else:
            upper_bound = mid_time
        predicted_time = mid_time

    return predicted_time

def gauss_jordan(a, b):
    
    ab = np.hstack([a, b.reshape(-1, 1)])
    n = len(ab)
    for i in range(n):
        ab[i] = ab[i] / ab[i, i]
        for j in range(n):
            if i != j:
                ab[j] = ab[j] - ab[j, i] * ab[i]
    return ab[:, -1]

def ball_paddle_collision_predictor(ball, ball_dx, ball_dy, paddle_y):
    a = np.array([[ball_dy, -1]], dtype=float)  
    b = np.array([paddle_y - ball.y], dtype=float)  
    solution = gauss_jordan(a, b)
    return solution[0]