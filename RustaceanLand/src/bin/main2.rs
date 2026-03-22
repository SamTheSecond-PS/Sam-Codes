struct Holder<'a, T> {
    refr: &'a T,
}

impl<'a, T: std::fmt::Debug> Holder<'a, T> {
    fn get_ref(&self) -> &T {
        &self.refr
    }
}

fn main() {
    let re: String = String::from("Heloo nnooo my pixxe");
    let sr: Holder<'_, String> = Holder { refr: &re };
    println!("{:?}", sr.get_ref());
}
