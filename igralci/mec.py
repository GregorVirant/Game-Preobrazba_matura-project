from priprava import *
hitrost = 5
visinaSkoka = -10
zamudaSkokaMax=0
sirinaPolovic=ekranSirina/2
lahkoNapada=True
rect=slikaMec.get_rect(centerx=sirinaPolovic,bottom=objects[0][0].top-1)
centerSlike = rect.center
napadZaostanekMax = 15

#narise
def draw(slikaM,rot):
    #global rect
    nov_mec = pygame.transform.rotate(slikaM,rot)
    #to pac rabmo zarad vrtenja
    rect = nov_mec.get_rect(center=centerSlike)
    #sam to ka se nerise se mal bol gor narise
    rect.top+5
    ekran.blit(nov_mec,rect)
    return rect