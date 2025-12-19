use rustysynth::{MidiFile, MidiFileSequencer, SoundFont, Synthesizer, SynthesizerSettings};
use std::sync::Arc; //Serve per usare rustysynth
use wasm_bindgen::prelude::*; //JS <-> WASM
use once_cell::sync::OnceCell;

static SOUNDFONT: OnceCell<Arc<SoundFont>> = OnceCell::new();

/// Carica il soundfont
#[wasm_bindgen]
pub fn load_sf2(sf2_data: &[u8]) {
    let mut sf2_cursor = std::io::Cursor::new(sf2_data);
    let sound_font = Arc::new(SoundFont::new(&mut sf2_cursor).unwrap());

    SOUNDFONT.set(sound_font).expect("SoundFont già caricato");
}

/// Crea un buffer audio e lo riempe renderizzando il file MIDI
#[wasm_bindgen] 
pub fn render_midi(midi_data: &[u8]) -> Vec<f32> {
    console_error_panic_hook::set_once();

    let sound_font = SOUNDFONT.get().expect("SoundFont non caricato");

    // Carica MIDI
    let mut midi_cursor = std::io::Cursor::new(midi_data);
    let midi_file = Arc::new(MidiFile::new(&mut midi_cursor).unwrap());

    // Crea sintetizzatore
    let settings = SynthesizerSettings::new(44100);
    let synth = Synthesizer::new(&sound_font, &settings).unwrap();

    // Crea sequenziatore
    let mut sequencer = MidiFileSequencer::new(synth);
    sequencer.play(&midi_file, false);

    // Calcola samples totali
    let sample_count = (settings.sample_rate as f64 * midi_file.get_length()) as usize;

    // Buffers audio sx e dx
    let mut left = vec![0.0f32; sample_count];
    let mut right = vec![0.0f32; sample_count];
    sequencer.render(&mut left, &mut right);

    // Valori interleaved per semplificare estrazione successivamente
    let mut out = vec![0.0f32; sample_count * 2];

    for i in 0..sample_count {
        let idx = i * 2;
        out[idx] = left[i];
        out[idx + 1] = right[i];
    }

    out
}


/// Macro usate nella funzione successiva
macro_rules! be_u32 {
    ($x:expr) => {
        u32::from_be_bytes($x.try_into().unwrap())
    };
}

macro_rules! be_u16 {
    ($x:expr) => {
        u16::from_be_bytes($x.try_into().unwrap())
    };
}

/// Controlla che i primi byte del file midi combacino con quelli richiesti dallo standard
#[wasm_bindgen]
pub fn check_midi_header(header: &[u8]) -> bool {
    if header.len() < 14
        || &header[0..4] != b"MThd"
        || be_u32!(header[4..8]) != 6
        || !(0..=2).contains(&be_u16!(header[8..10]))
        || be_u16!(header[10..12]) == 0
    {
        return false;
    }

    true
}
