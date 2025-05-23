import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))



def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：判定結果（横、縦）
    画面外ならTrue、画面外ならFalse
    """
    yoko, tate = True, True  #  横, 縦判定用変数
    #左右判定
    if rct.left < 0 or WIDTH < rct.right: # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: # 縦方向判定
        tate = False
    return yoko, tate



def gameover(screen: pg.Surface) -> None:    #  演習１
    fonto = pg.font.Font(None, 80)
    
    img = pg.image.load("fig/3.png")
    sikaku = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(sikaku, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    sikaku.set_alpha(100)
    screen.blit(sikaku, [0, 0])
    img2 = pg.image.load("fig/8.png")
    img2_rct = img2.get_rect()
    img2_rct.center = WIDTH/4, HEIGHT/2
    img2_rct2 = img2.get_rect()
    img2_rct2.center = WIDTH/1.35, HEIGHT/2
    txt = fonto.render("GameOver", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH/2, HEIGHT/2

    screen.blit(img2, img2_rct)
    screen.blit(img2, img2_rct2)
    screen.blit(txt, txt_rct)

    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:  #  演習２
    tmr = 5000
    sbb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)


        return
    

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    #こうかとん初期化
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    #爆弾初期化
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bb_img.set_colorkey((0, 0, 0))
    clock = pg.time.Clock()
    tmr = 0
    vx, vy = +5, +5
    
    
    



    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):  #  こうかとんRectと爆弾Rectが重なったら
            gameover(screen)
            
            return
            

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  #左右方向
                sum_mv[1] += mv[1]  #上下方向


        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  #画面外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #  画面内に戻す
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  #爆弾の速度
        yoko, tate = check_bound(bb_rct)
        if not yoko: #  左右どちらか
            vx *= -1
        if not tate: #  上下どちらか
            vy *= -1

        bb_imgs, bb_accs = init_bb_imgs()
        avx = vx*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]

        screen.blit(bb_img, bb_rct)  #爆弾の描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
