from priprava import *
hitrost = 4
visinaSkoka = 0
zamudaSkokaMax=0
sirinaPolovic=ekranSirina/2
lahkoNapada=False
rect=slikaZoga.get_rect(centerx=sirinaPolovic,bottom=objects[0][0].top-1)
centerSlike = rect.center
napadZaostanekMax = 10

#narise
def draw(rot):
    #tu se pac zarotira
    nova_zoga = pygame.transform.rotate(slikaZoga,rot)
    rect = nova_zoga.get_rect(center=centerSlike)
    rect.top+5
    #se narise
    ekran.blit(nova_zoga,rect)
    return rect