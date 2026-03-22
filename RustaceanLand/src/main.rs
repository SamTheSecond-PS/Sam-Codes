struct Character {
    name: String,
    health: i32,
    mana: i32,
    damage: i32,
    xp: i32,
    req: i32,
    giv_exp: i32,
    heal: i32,
    lvl: i32,
}

impl Character {
    fn new(name: &str) -> Self {
        let exp = 10;
        let dmg = exp * 2;
        let mana = dmg * 2;
        let reqq = exp * 4;
        let hlt = (dmg + exp) * 2;
        let lvl = 0;
        let giv_exp = hlt + dmg;
        let heal = hlt - exp;

        Self {
            name: name.to_string(),
            health: hlt,
            mana: mana,
            damage: dmg,
            xp: exp,
            req: reqq,
            giv_exp: giv_exp,
            heal: heal,
            lvl: lvl,
        }
    }
}

impl Character {
    fn level_up<'a>(&mut self) -> () {
        if self.req <= self.xp {
            let nl = self.lvl / self.req;
            println!("Levelled up! {} -> {}", self.lvl, nl);
            self.lvl = nl;
        } else {
            println!("Exp too low!");
        }
    }
}

impl Character {
    fn attack<'a>(self, mut ch: Character) {
        ch.health -= self.damage;
    }
}

impl Character {
    fn heal(&mut self) {
        self.health += self.heal;
    }
}

fn main() {
    let mut sam = Character::new("sam");
    let evil_enemy = Character::new("Villian");
    sam.level_up();
    sam.attack(evil_enemy);
}
