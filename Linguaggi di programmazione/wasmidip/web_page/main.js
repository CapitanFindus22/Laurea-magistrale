//Importa il codice WASM generato
import init, { load_sf2, check_midi_header, render_midi } from "../pkg/wasmidip.js";
await init();

//Crea parte audio e carica soundfont
const audioCtx = new AudioContext();
let sf2Data = null;

try {
    sf2Data = await fetch("web_page/GeneralUser-GS.sf2").then(r => r.arrayBuffer());
    load_sf2(new Uint8Array(sf2Data));
} catch (error) {
    console.log(error);
    alert("Soundfont non caricato");
}

// Astrazione per semplificare il codice successivo
class MidiPlayer {
    constructor() {

        this.audioCtx = audioCtx;
        this.gainNode = this.audioCtx.createGain();
        this.gainNode.connect(this.audioCtx.destination);
        this.gainNode.gain.value = parseFloat(document.getElementById("volume").value);

        this.audioBuffer = null;

        this.src = null;

        this.isPlaying = false;

        this.startTime = 0;
        this.pauseTime = 0;

    }

    // Crea sorgente audio dal buffer
    _createSource() {
        this.src = this.audioCtx.createBufferSource();
        this.src.buffer = this.audioBuffer;

        this.src.connect(this.gainNode);

        this.src.onended = () => {

            if (this.isPlaying && this.currentTime >= this.audioBuffer.duration) {

                document.getElementById("play").disabled = false;
                document.getElementById("pause").disabled = true;
                document.getElementById("stop").disabled = true;

                this.startTime = 0;
                this.pauseTime = 0;
                this.src = null;
                this.isPlaying = false;

            }

        }
    }

    // Carica buffer
    loadBuffer(buffer) {
        this.stop();
        this.audioBuffer = buffer;
    }

    // Riproduci
    play() {

        document.getElementById("play").disabled = true;
        document.getElementById("pause").disabled = false;
        document.getElementById("stop").disabled = false;

        if (!this.src) {
            this._createSource();
            this.src.start(0, this.pauseTime);
            this.isPlaying = true;
            this.startTime = this.audioCtx.currentTime - this.pauseTime;
        }
    }

    // Metti in pausa
    pause() {

        if (!this.isPlaying) return;

        document.getElementById("pause").disabled = true;
        document.getElementById("play").disabled = false;

        this.src.stop();
        this.src = null;
        this.isPlaying = false;
        this.pauseTime = this.audioCtx.currentTime - this.startTime;

    }

    // Ferma
    stop() {

        document.getElementById("pause").disabled = true;
        document.getElementById("play").disabled = false;
        document.getElementById("stop").disabled = true;


        if (this.src) {
            this.src.stop();
            this.src = null;
        }

        this.isPlaying = false;
        this.startTime = 0;
        this.pauseTime = 0;

    }

    set volume(value) {
        this.gainNode.gain.value = value;
    }

    get currentTime() {
        if (this.isPlaying) {
            return this.audioCtx.currentTime - this.startTime;
        }
        return this.pauseTime;
    }

}

// Crea il buffer audio (tramite WASM) per la riproduzione
async function renderMidiFile(file) {

    // Apri file MIDI
    const midiData = await file.arrayBuffer();
    const mData = new Uint8Array(midiData);

    // Controlla struttura file
    if (check_midi_header(mData.subarray(0, 14))) {

        // Chiama funzione di render WASM
        const samples = render_midi(mData);

        // Spezza buffer interleaved in canali SX e DX
        const buffer = new AudioBuffer({
            length: samples.length / 2,
            sampleRate: 44100,
            numberOfChannels: 2
        });

        const L = buffer.getChannelData(0);
        const R = buffer.getChannelData(1);

        for (let i = 0; i < samples.length / 2; i++) {
            L[i] = samples[i * 2];
            R[i] = samples[i * 2 + 1];
        }

        return buffer;

    }

    console.error("Formato file non valido");

    return null;
}

const player = new MidiPlayer();

// Input file
document.getElementById("midiFile").addEventListener("change", async (ev) => {

    if (sf2Data) {

        const file = ev.target.files[0];

        if (!file) return;

        document.body.style.cursor = "wait";
        document.getElementById("loading").hidden = false;

        if (player) player.stop();

        const audioBuffer = await renderMidiFile(file);

        if (!audioBuffer) return;

        player.loadBuffer(audioBuffer);

        document.getElementById("loading").hidden = true;
        document.body.style.cursor = "default";

        document.getElementById("play").disabled = false;
        document.getElementById("volume").disabled = false;

    }

    else alert("Soundfont non presente");

});

// Controlli riproduzione
document.getElementById("play").onclick = () => player?.play();
document.getElementById("pause").onclick = () => player?.pause();
document.getElementById("stop").onclick = () => player?.stop();
document.getElementById("volume").oninput = (ev) =>
    player && (player.volume = ev.target.value);

// Mostra l'andamento della riproduzione
const progress = document.getElementById("time");
function updateProgress() {

    if (player && player.audioBuffer) {
        const current = player.currentTime;
        const duration = player.audioBuffer.duration;
        const percent = (current / duration) * 100;
        progress.value = percent;
        progress.textContent = Math.floor(percent) + "%";
    }
    requestAnimationFrame(updateProgress);
}
requestAnimationFrame(updateProgress);
