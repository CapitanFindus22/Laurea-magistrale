use rustysynth::{SoundFont, Synthesizer, SynthesizerSettings, MidiFile, MidiFileSequencer};
use std::fs::File;
use std::sync::Arc;
use rodio::{OutputStream, Sink};

fn main() {
    // Apri lo stream audio
    let (_stream, stream_handle) = OutputStream::try_default().unwrap();
    let sink = Sink::try_new(&stream_handle).unwrap();

    // Carica SoundFont
    let mut sf2 = File::open("GeneralUser-GS.sf2")
        .expect("SoundFont non trovato");
    let sound_font = Arc::new(SoundFont::new(&mut sf2).unwrap());

    // Carica il file MIDI
    let mut midi_file = File::open("a.mid").expect("File MIDI non trovato");
    let midi = Arc::new(MidiFile::new(&mut midi_file).unwrap());

    // Crea sintetizzatore
    let settings = SynthesizerSettings::new(44100);
    let synth = Synthesizer::new(&sound_font, &settings).unwrap();
    let mut sequencer = MidiFileSequencer::new(synth);

    // Play del MIDI (senza loop)
    sequencer.play(&midi, false);

    // Genera il buffer audio
    let sample_count = (settings.sample_rate as f64 * midi.get_length()) as usize;
    let mut left = vec![0.0_f32; sample_count];
    let mut right = vec![0.0_f32; sample_count];
    sequencer.render(&mut left[..], &mut right[..]);

    // Combina i canali in un unico buffer stereo
    let samples: Vec<i16> = left.iter().zip(right.iter())
        .flat_map(|(l,r)| {
            let li = (l * 32767.0) as i16;
            let ri = (r * 32767.0) as i16;
            vec![li, ri]
        })
        .collect();

    // Crea un source da rodio e riproduci
    let source = rodio::buffer::SamplesBuffer::new(2, 44100, samples);
    sink.append(source);

    // Attendi la fine della riproduzione
    sink.sleep_until_end();
}
