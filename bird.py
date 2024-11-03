from blessed import Terminal
import time
import random
import argparse

# 初始化常量
term = Terminal()
BIRD = ">"
PIPE = "|"
GAP = 8
GRAVITY = 1
BIRD_JUMP_VELOCITY = -2
PIPE_DISTANCE = 30
BASE_SPEED = 0.1  # 基础速度

class FlappyBirdGame:
    def __init__(self):
        self.bird_y = (term.height - 1) // 2  # 控制台高度减1
        self.bird_x = 5
        self.bird_velocity = 0
        self.pipes = [self.create_pipe()]  # 确保游戏开始时有管道
        self.score = 0
        self.game_over = False

    def create_pipe(self):
        """创建一个新的管道"""
        pipe_y = random.randint(1, term.height - GAP - 2)  # 控制台高度减2，以避免越界
        return [term.width, pipe_y]

    def update_bird_position(self):
        """更新小鸟的位置并检查是否游戏结束"""
        self.bird_y += self.bird_velocity
        if self.bird_y < 0:
            self.bird_y = 0
        elif self.bird_y >= term.height - 1:  # 控制台高度减1
            self.game_over = True

    def draw_bird(self):
        """绘制小鸟"""
        print(term.move(self.bird_y, self.bird_x) + BIRD)

    def draw_pipes(self):
        """绘制管道"""
        for pipe_x, pipe_y in self.pipes:
            if pipe_x > 0:
                for y in range(pipe_y):
                    print(term.move(y, pipe_x) + PIPE)
                for y in range(pipe_y + GAP, term.height - 1):  # 控制台高度减1
                    print(term.move(y, pipe_x) + PIPE)

    def check_collision(self):
        """检查小鸟是否与管道碰撞"""
        for pipe_x, pipe_y in self.pipes:
            if pipe_x == self.bird_x and (self.bird_y < pipe_y or self.bird_y >= pipe_y + GAP):
                self.game_over = True

    def update_pipes(self):
        """更新管道位置并检测得分"""
        new_pipes = []
        for pipe_x, pipe_y in self.pipes:
            if pipe_x > 0:
                new_pipes.append([pipe_x - 1, pipe_y])  # 管道向左移动
                if pipe_x == self.bird_x:
                    self.score += 1  # 计分
        self.pipes = new_pipes

    def main_loop(self, auto=False):
        """游戏主循环"""
        with term.cbreak(), term.hidden_cursor():
            while not self.game_over:
                print(term.clear)
                print(term.move(0, 0) + f"得分: {self.score}")  # 打印得分

                # 自动或手动控制小鸟上升
                if auto:
                    for pipe_x, pipe_y in self.pipes:
                        if pipe_x > self.bird_x:
                            gap_center = pipe_y + GAP // 2  # 管道间隙的中心
                            self.bird_velocity = BIRD_JUMP_VELOCITY if self.bird_y >= gap_center else self.bird_velocity + GRAVITY
                            break
                    else:
                        self.bird_velocity += GRAVITY
                else:
                    key = term.inkey(timeout=0.1)
                    self.bird_velocity = BIRD_JUMP_VELOCITY if key == " " else self.bird_velocity + GRAVITY

                self.update_bird_position()

                # 创建新管道
                if len(self.pipes) == 0 or self.pipes[-1][0] < term.width - PIPE_DISTANCE:
                    self.pipes.append(self.create_pipe())

                self.draw_bird()
                self.update_pipes()
                self.draw_pipes()
                self.check_collision()

                # 根据得分调整游戏速度
                sleep_time = max(BASE_SPEED - self.score * 0.005, 0.02)  # 最小为0.02秒
                time.sleep(sleep_time)

            # 显示游戏结束画面
            print(term.move(term.height // 2, term.width // 2 - 5) + "游戏结束!")
            print(term.move(term.height // 2 + 1, term.width // 2 - 7) + f"你的得分: {self.score}")
            time.sleep(2)

if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description='Flappy Bird 克隆版.')
    parser.add_argument('-auto', action='store_true', help='以自动模式运行.')
    args = parser.parse_args()

    game = FlappyBirdGame()
    game.main_loop(auto=args.auto)
