#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>
#include <ctype.h>
#include <time.h>

// --- Constante --- //

#define NB_COLLONE 28
#define NB_LIGNE 31

const char GOMME = '.';
const char SUPER_GOMME = 'O';
const int CERISE_TIME = 30;

// --- Nouveau type --- //

typedef char t_grille[NB_LIGNE][NB_COLLONE]; // Type répresentant la grille
typedef int t_tab2[2]; // Type servant a répresneter les coordonnées

const t_tab2 PACMAN = {23, 13}; // Déclaration des position de départ
const t_tab2 BLINKY = {11, 13};
const t_tab2 INKY = {14, 11};
const t_tab2 PINKY = {14, 13};
const t_tab2 CLYDE = {14, 15};
const t_tab2 CERISE = {17, 14}; // Positionnement de la cerise
const t_tab2 CERISE_SPAWN = {70, 170};

// --- Déclaration des variables global --- //

int playerPoint = 0;
int nbLive = 1;
// Changer au chargement du plateau
int nbGommesRemaining = 0;
int ceriseTimer = 0;
int ceriseSpawn70 = 0;
int ceriseSpawn170 = 0;
int nbGommesEat = 0;
char toucheCourant = ' ';
char touchePlay = 'q';
bool win = false;

t_tab2 pacman = {PACMAN[0], PACMAN[1]}; // Inintialisation des positions de départ
t_tab2 blinky = {BLINKY[0], BLINKY[1]};
t_tab2 inky = {INKY[0], INKY[1]};
t_tab2 pinky = {PINKY[0], PINKY[1]};
t_tab2 clyde = {CLYDE[0], CLYDE[1]};
t_tab2 direction = {0, -1};
t_tab2 dirInky = {0, 0};   // direction actuelle des fantomes (0, 0 = à l'arrêt)
t_tab2 dirPinky = {0, 0};
t_tab2 dirClyde = {0, 0};

// --- Déclaration des fonctions --- //

int kbhit();
int chargerPlateau(t_grille plateau, char nomFichier[]);
void finDePartie(t_grille grille, char message[10]);
int coupIsValid(t_grille grille, t_tab2 pacman, char touche);
void afficherGrille(t_grille grille);
void movePacman(t_grille grille);
void spawnCerise(t_grille grille);
void blinkyMove(t_grille grille);
char randomMove();
void formatTouche(char touche, t_tab2 dir);
int directionIsValid(t_grille grille, t_tab2 pos, t_tab2 dir);
void otherGhostMove(t_grille grille, t_tab2 ghost, t_tab2 direction);
void fantomeMove(t_grille grille);
void update(t_grille grille);
int processTouche(char touche);
void manageTouches(t_grille grille);
void boucleJeu(t_grille grille);

// --- Début du code --- //

// Appel toutes les fonction afin de faire tourner le jeu
// Charge le plateau, config la grille et lance la boucle de jeu
int main() {

    t_grille grille;

    srand(time(NULL)); // initialise le hasard pour les fantomes
    //Première affiche, quand le jeu attend 3 secondes
    // Remplissage du plateau et chargement de la varialbe nbGommeRemaining
    nbGommesRemaining = chargerPlateau(grille, "grillePacman.txt");
    printf("READY \n");
    afficherGrille(grille);
    usleep(3000000);
    //Lance la boucle de jeu
    boucleJeu(grille);
    //Quand le joueur a perdue
    if (nbLive == 0) {
        finDePartie(grille, "Game Over ! \n");
    }
    if (nbGommesRemaining == 0) {
        finDePartie(grille, "Win !   \n");
    }

    return EXIT_SUCCESS;

}

int kbhit() {
    // la fonction retourne :
    // 1 si un caractere est present
    // 0 si pas de caractere présent
    int unCaractere=0;
    struct termios oldt, newt;
    int ch;
    int oldf;

    // mettre le terminal en mode non bloquant
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);
    oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
    fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);

    ch = getchar();

    // restaurer le mode du terminal
    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    fcntl(STDIN_FILENO, F_SETFL, oldf);

    if(ch != EOF){
        ungetc(ch, stdin);
        unCaractere=1;
    }
    return unCaractere;
}

// fonction qui charge les données du fichier dans le tableau
// la fonction retourne le nombre total de gommes et super-gommes
int chargerPlateau(t_grille plateau, char nomFichier[]){
	FILE * f;
	char finDeLigne;
	int resultat = 0;

	f = fopen(nomFichier, "r");
	if (f==NULL) {
		printf("Erreur sur le fichier %s\n", nomFichier);
	} else {
		for (int ligne=0 ; ligne<NB_LIGNE ; ligne++){
            for (int colonne=0 ; colonne<NB_COLLONE ; colonne++){
                fread(&plateau[ligne][colonne], sizeof(char), 1, f);
				if (plateau[ligne][colonne]==GOMME || plateau[ligne][colonne]==SUPER_GOMME){
					resultat++;
				}
            }
            fread(&finDeLigne, sizeof(char), 1, f);
        }
        fclose(f);
	}
	return resultat;
}

//Fonction d'affichage lorsque la partie est finie
void finDePartie(t_grille grille, char message[10]) {
    system("clear");
    usleep(2000000);
    printf("Points: %d\nNombre de gomme restant : %d\n", playerPoint, nbGommesRemaining);
    printf(message);
    // Affiche de chaque case de la grille
    for (int i = 0; i < NB_LIGNE; i++) {
        for (int j = 0; j < NB_COLLONE; j++) {
            printf("%c", grille[i][j]);
        }
        printf("\n");
    }
}

// Sert a verifier si un coup est valide avant de le jouer
// Retourne 1 si le coup est possible
// Retourne 0 si le coup est impossible
int coupIsValid(t_grille grille, t_tab2 pacman, char touche) {

    t_tab2 directionLocal;
    t_tab2 newPacman;

    switch (touche) {
        case 'z':
        directionLocal[0] = -1;
        directionLocal[1] = 0;
        break;
        case 's':
        directionLocal[0] = 1;
        directionLocal[1] = 0;
        break;
        case 'q':
        directionLocal[0] = 0;
        directionLocal[1] = -1;
        break;
        case 'd':
        directionLocal[0] = 0;
        directionLocal[1] = 1;
        break;
        default:
        directionLocal[0] = 0;
        directionLocal[1] = -1;
        break;
    }

    newPacman[0] = (pacman[0]+directionLocal[0] + NB_LIGNE) % NB_LIGNE;
    newPacman[1] = (pacman[1]+directionLocal[1] + NB_COLLONE) % NB_COLLONE;

    if (grille[newPacman[0]][newPacman[1]] != '#' && grille[newPacman[0]][newPacman[1]] != '-') {
        return 1;
    }
    else {
        return 0;
    }

}

// Sert a afficher la grille et les infos général sur la partie
void afficherGrille(t_grille grille) {
    // Affichage des informations général :
    printf("Points: %d\nNombre de gomme restant : %d\n", playerPoint, nbGommesRemaining);
    // Affiche de chaque case de la grille
    for (int i = 0; i < NB_LIGNE; i++) {
        for (int j = 0; j < NB_COLLONE; j++) {
            if (pacman[0] == i && pacman[1] == j) printf("%c", 'G');
            else if (blinky[0] == i && blinky[1] == j) printf("%c", 'B');
            else if (inky[0] == i && inky[1] == j) printf("%c", 'I');
            else if (pinky[0] == i && pinky[1] == j) printf("%c", 'P');
            else if (clyde[0] == i && clyde[1] == j) printf("%c", 'C');
            else {
                printf("%c", grille[i][j]);
            }
        }
        printf("\n");
    }
}

// Gestion des déplacement de pacman
void movePacman(t_grille grille) {
    t_tab2 newPacman;
    // Calcul des nouvelles coordonnées de pacman
    newPacman[0] = (pacman[0] + direction[0] + NB_LIGNE) % NB_LIGNE;
    newPacman[1] = (pacman[1] + direction[1] + NB_COLLONE) % NB_COLLONE;

    // Calcul de sa case future dans la grille
    char caseFuture = grille[newPacman[0]][newPacman[1]];

    // Regarde si la prochaine case est possible
    if (caseFuture != '#' && caseFuture != '-') {
        // Vérifie que la case n'est pas occupé par un fantome
        if ((blinky[0] == newPacman[0] && blinky[1] == newPacman[1]) ||
            (inky[0] == newPacman[0] && inky[1] == newPacman[1]) ||
            (pinky[0] == newPacman[0] && pinky[1] == newPacman[1]) ||
            (clyde[0] == newPacman[0] && clyde[1] == newPacman[1])) {
            nbLive -= 1;
        // Vérifie si la case n'est pas une gomme
        } else if (caseFuture == '.') {
            playerPoint += 10;
            nbGommesRemaining -= 1;
            nbGommesEat ++;
        // Vérifie si la case n'est pas une super-pacgomme
        } else if (caseFuture == 'O') {
            playerPoint += 50;
            nbGommesRemaining -= 1;
            nbGommesEat ++;
        }
        // Verifie si la case n'est pas une cerise
        else if (caseFuture == 'c') {
            if (ceriseSpawn70) {
                if (ceriseSpawn170) {
                    playerPoint += 100;
                }
                else {
                    playerPoint += 100;
                }
            }
        }

        // On vide juste la case mangée.
        grille[newPacman[0]][newPacman[1]] = ' ';

        //Applique les nouvelles coordonée de pacman
        pacman[0] = newPacman[0];
        pacman[1] = newPacman[1];
    }
}

// Gestion de l'apparition des cerises
void spawnCerise(t_grille grille) {
    // Verifie si les conditions pour la première cerise on été atteinte et qu'elle n'est pas deja apparue
    if (nbGommesEat >= CERISE_SPAWN[0] && !ceriseSpawn70) {
        grille[CERISE[0]][CERISE[1]] = 'c';
        ceriseTimer = CERISE_TIME;
        ceriseSpawn70 = 1;
    }
    // Idem que pour la première cerise
    else if (nbGommesEat >= CERISE_SPAWN[1] && !ceriseSpawn170) {
        grille[CERISE[0]][CERISE[1]] = 'c';
        ceriseTimer = 54;
        ceriseSpawn170 = 1;
    }

    // Gestion du cooldown des cerises
    if (ceriseTimer > 0) {
        ceriseTimer--;

        // Fait disparaitre la cerise si son cooldown atteint zéro
        if (ceriseTimer == 0) {
            if (grille[CERISE[0]][CERISE[1]] == 'c') {
                grille[CERISE[0]][CERISE[1]] = ' ';
            }
        }
    }
}

// Gestion des déplacements de blinky
void blinkyMove(t_grille grille) {
    t_tab2 move = {0, 0};

    // Calcul la distance entre pacman et blinky
    int diffX = pacman[0] - blinky[0];
    int diffY = pacman[1] - blinky[1];

    // Si pacman n'est pas sur la même ligne que blinky
    if (diffX != 0) {
        move[0] = (diffX > 0) ? 1 : -1; // si la différence est supérieure a 0 on se déplace vers le bas sinon vers le haut
    // Sinon si pacman n'est pas sur la même colonne
    } else if (diffY != 0) {
        move[1] = (diffY > 0) ? 1 : -1; // si la différence est supérieure a 0 on se déplace vers la droite sinon vers la gauche
    }

    // Calcul des prochaines coordonnées de blinky
    int nextX = (blinky[0] + move[0] + NB_LIGNE) % NB_LIGNE;
    int nextY = (blinky[1] + move[1] + NB_COLLONE) % NB_COLLONE;

    // Vérifie si la case est un mur et que pacman n'est pas sur la même colonne, si c'est le cas blinky essaye de contourner en se déplaçant horizontalement
    if ((grille[nextX][nextY] == '#' || grille[nextX][nextY] == '-') && diffY != 0) {
        move[0] = 0;
        move[1] = (diffY > 0) ? 1 : -1;
        // calcul des prochaines coordonnées de blinky
        nextX = (blinky[0] + move[0] + NB_LIGNE) % NB_LIGNE;
        nextY = (blinky[1] + move[1] + NB_COLLONE) % NB_COLLONE;
    }

    // Récupère le contenu de la case ou blinky veut aller
    char futurCase = grille[nextX][nextY];

    // Verifie si la case n'est pas occupé par pacman sinon ca le tue
    if (nextX == pacman[0] && nextY == pacman[1]) {
        nbLive -= 1;
    }
    // Vérifie que la case n'est ni un mur ni la porte de la maison des fantômes
    else if (futurCase != '#' && futurCase != '-') {
        // Supprime l'ancienne case de blinky
        // grille[blinky[0]][blinky[1]] = ' ';

        // Applique les nouvelles coordonnées de blinky
        blinky[0] = nextX;
        blinky[1] = nextY;

        // Affiche blinky sur sa nouvelle case
        // grille[blinky[0]][blinky[1]] = 'B';
    }
}

// Tire une direction au hasard et la retourne sous forme de touche (z, s, q ou d)
char randomMove() {
    const char TOUCHES[4] = {'z', 's', 'q', 'd'};
    return TOUCHES[rand() % 4];
}

// Remplit dir avec la direction correspondant à une touche (z, s, q ou d)
void formatTouche(char touche, t_tab2 dir) {
    dir[0] = 0;
    dir[1] = 0;
    switch (touche) {
        case 'z': dir[0] = -1; break;
        case 's': dir[0] = 1; break;
        case 'q': dir[1] = -1; break;
        case 'd': dir[1] = 1; break;
    }
}

// Retourne 1 si un fantome placé en pos peut avancer dans la direction dir
int directionIsValid(t_grille grille, t_tab2 pos, t_tab2 dir) {
    int x = (pos[0] + dir[0] + NB_LIGNE) % NB_LIGNE;
    int y = (pos[1] + dir[1] + NB_COLLONE) % NB_COLLONE;
    return grille[x][y] != '#' && grille[x][y] != '-';
}

// Gestion des déplacements de inky, pinky et clyde
void otherGhostMove(t_grille grille, t_tab2 ghost, t_tab2 direction) {
    t_tab2 move = {0, 0};

    if (ghost[0] > 11 && ghost[0] < 16 && ghost[1] > 10 && ghost[1] < 17) {
        // Le fantome est dans la maison (lignes 12 à 15, colonnes 11 à 16) : il va vers la colonne 13 puis monte
        if (ghost[1] < 13) {
            move[1] = 1;
        } else if (ghost[1] > 13) {
            move[1] = -1;
        } else {
            move[0] = -1;
        }
        // Il n'a pas de direction tant qu'il n'est pas sorti
        direction[0] = 0;
        direction[1] = 0;
    } else {
        if ((direction[0] == 0 && direction[1] == 0) || !directionIsValid(grille, ghost, direction)) {
            int essais = 0;
            do {
                formatTouche(randomMove(), direction);
                essais++;
            } while (!directionIsValid(grille, ghost, direction) && essais < 20);
        }
        // Il avance dans sa direction si la case est libre
        if (directionIsValid(grille, ghost, direction)) {
            move[0] = direction[0];
            move[1] = direction[1];
        }
    }

    // Calcul des nouvelles coordonnées du fantome (avec le tunnel)
    int nextX = (ghost[0] + move[0] + NB_LIGNE) % NB_LIGNE;
    int nextY = (ghost[1] + move[1] + NB_COLLONE) % NB_COLLONE;

    // Si le fantome arrive sur pacman, pacman perd une vie
    if (nextX == pacman[0] && nextY == pacman[1]) {
        nbLive -= 1;
    } else {
        ghost[0] = nextX;
        ghost[1] = nextY;
    }
}

// Gestion des déplacement de tout les fantômes
void fantomeMove(t_grille grille) {

    // GEstion spécial de blinky
    blinkyMove(grille);

    // Gestion des autres fantomes
    // Gestion de Inky
    otherGhostMove(grille, inky, dirInky);
    // Gestion de Pinky
    otherGhostMove(grille, pinky, dirPinky);
    // Gestion de Clyde
    otherGhostMove(grille, clyde, dirClyde);
}

// Appel tout les fonctions qui gère l'update du jeu
void update(t_grille grille) {
    spawnCerise(grille);
    movePacman(grille);
    fantomeMove(grille);
}

// Gestion des touches appuyé
int processTouche(char touche) {
    int res = 0;
    switch (touche) {
        case 'z':
            direction[0] = -1;
            direction[1] = 0;
            res = 1;
        break;
        case 's':
            direction[0] = 1;
            direction[1] = 0;
            res = 1;
        break;
        case 'q':
            direction[0] = 0;
            direction[1] = -1;
            res = 1;
        break;
        case 'd':
            direction[0] = 0;
            direction[1] = 1;
            res = 1;
        break;
        default:
            break;
    }
    return res;
}

// Récupère les touches appuyé et vérifie si ses coups sont valide
void manageTouches(t_grille grille) {
    // Recupère la touche
    if (kbhit()) {

        toucheCourant = tolower(getchar());

    }
    // Vérifie si le coup est valide et le joue dans ce cas
    if (coupIsValid(grille, pacman, toucheCourant) == 1) {

        processTouche(toucheCourant);
        touchePlay = toucheCourant;

    }
}

// Boucle de jeu, joue les fonctions tant que pacman est en vie
void boucleJeu(t_grille grille) {
    //Tourne tant que pacman est en vie et que pacman n'as pas mangé toute les gommes
    while (nbLive > 0 && !win) {
        system("clear");

        manageTouches(grille);
        update(grille);
        afficherGrille(grille);

        // Detecte quand pacman a mange toute les gommes
        if (nbGommesRemaining == 0) {
            win = true;
        }

        usleep(200000);
    }
}
