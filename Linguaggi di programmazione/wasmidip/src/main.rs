use crate::parser::*;

mod parser;

fn main() {
    let f: MIDIFile = MIDIFile::new("./src/a.mid");

    println!(
        "Formato: {}, Numero tracce: {}, Divisione: {}",
        f.file_type,
        f.tracks_num,
        f.division.values()
    );

    println!("{:?}", f.tracks[0].display());

}
