import * as readline from 'node:readline';

readline.emitKeypressEvents(process.stdin);
if (process.stdin.isTTY) process.stdin.setRawMode(true);

const NB_COl = 4;
const NB_LIG = 4

type t_tab = Number[][];
type coord = [number, number];


let grille: t_tab = [];
let move: Number;

for (let i = 0; i < NB_LIG; i++) {
    grille[i] = [];
    for (let j = 0; j < NB_COl; j++) {
        grille[i][j] = 0
    }
}

function generateTile(): coord  {

    let x, y;
    x = Math.floor(Math.random() * NB_COl);
    y = Math.floor(Math.random() * NB_LIG);

    if (grille[x][y] == 0) return [x, y];
    else return generateTile();

}

function placeTile(): void {
    
    let random: Number = Math.floor(Math.random() * 10);

    if (move == 0) {
        
        var tile1: coord = generateTile();

        if (random == 0) grille[tile1[0]][tile1[1]] = 4;
        else grille[tile1[0]][tile1[1]] = 2;
        
        var tile2: coord = generateTile();
        let random2: Number = Math.floor(Math.random() * 10);

        if (random2 == 0) grille[tile2[0]][tile2[1]] = 4;
        else grille[tile2[0]][tile2[1]] = 2;

    }
    else {

        var tile: coord = generateTile();

        if (random == 0) grille[tile[0]][tile[1]] = 4;
        else grille[tile[0]][tile[1]] = 2;

    }
}

function afficherGrille(): void {
    console.clear();
    console.table(grille);
}

function jouerCoup(coup: coord): void {

    for (let i = 0; i < NB_COl; i++) {
        for (let j = 0; j < NB_LIG; j++) {

            var x = i+coup[1];
            var y = j+coup[0];

            if (x < NB_COl && x >= 0 && y < NB_LIG && NB_LIG >= 0) {
                
                let tile = grille[i][j];

                let tileManage = grille[x][j];
                tileManage
            }

        }

    }
}

function main() {

    move = 0;

    placeTile();
    afficherGrille();

    process.stdin.on("keypress", (_str, key) => {
        if (key.ctrl && key.name === "c") process.exit();

        if (key.name === "up")    jouerCoup([-1, 0]);
        if (key.name === "down")  jouerCoup([1, 0]);
        if (key.name === "left")  jouerCoup([0, -1]);
        if (key.name === "right") jouerCoup([0, 1]);
    });

}

main()