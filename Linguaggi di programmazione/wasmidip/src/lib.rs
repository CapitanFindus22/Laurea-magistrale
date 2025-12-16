use rustysynth::{MidiFile, MidiFileSequencer, SoundFont, Synthesizer, SynthesizerSettings};
use std::sync::Arc; //Serve per usare rustysynth
use wasm_bindgen::prelude::*; //JS <-> WASM

#[wasm_bindgen] //Esportabile in JS
pub fn render_midi(sf2_data: &[u8], midi_data: &[u8]) -> Vec<f32> {
    console_error_panic_hook::set_once();

    // Carica soundfont
    let mut sf2_cursor = std::io::Cursor::new(sf2_data);
    let sound_font = Arc::new(SoundFont::new(&mut sf2_cursor).unwrap());

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

#[wasm_bindgen]
extern "C" {
    #[wasm_bindgen(js_namespace = console)]
    fn log(s: &str);
}

#[wasm_bindgen]
pub fn check_header(header: &[u8]) -> bool {
    if header.len() < 14 || &header[0..4] != b"MThd" || &header[4..8] != [0x00, 0x00, 0x00, 0x06] {
        return false;
    }

    true
}
