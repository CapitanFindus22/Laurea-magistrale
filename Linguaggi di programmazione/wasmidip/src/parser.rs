use std::fs;


/**
 * https://web.archive.org/web/20141227205754/http://www.sonicspot.com:80/guide/midifiles.html
 */
#[derive(Debug, Clone, Copy)]
pub enum TimeDivision {
    PPQ(u16),
    SMPTE { frame_rate: i8, ticks_per_frame: u8 },
}

impl TimeDivision {
    pub fn from_u16(raw: u16) -> Self {
        if raw & 0x8000 == 0 {
            TimeDivision::PPQ(raw)
        } else {
            let fps = (raw >> 8) as i8;
            let ticks = (raw & 0xFF) as u8;
            TimeDivision::SMPTE {
                frame_rate: fps,
                ticks_per_frame: ticks,
            }
        }
    }

    pub fn values(&self) -> String {
        match self {
            TimeDivision::PPQ(ticks) => format!("PPQ: {} ticks per quarter note", ticks),
            TimeDivision::SMPTE {
                frame_rate,
                ticks_per_frame,
            } => {
                format!(
                    "SMPTE: {} fps, {} ticks per frame",
                    frame_rate, ticks_per_frame
                )
            }
        }
    }
}

pub struct Track {

    pub num: usize,
    pub size: u32,
    pub data: Vec<u8>,

}

impl Track {
    
    pub fn display(&self) -> String {

        format!("Traccia {}, Dimensione {}: {:?}", self.num, self.size, self.data)

    }

}

pub struct MIDIFile {
    pub file_type: u8,
    pub tracks_num: u16,
    pub division: TimeDivision,
    pub tracks: Vec<Track>,
}

impl MIDIFile {
    pub fn new(path: &str) -> Self {
        let data = fs::read(path).unwrap();

        if &data[0..4] != b"MThd" {
            panic!("file non valido");
        }

        let file_type = u16::from_be_bytes([data[8], data[9]]) as u8;
        let tracks_num = u16::from_be_bytes([data[10], data[11]]);
        let raw_division = u16::from_be_bytes([data[12], data[13]]);
        let mut tracks:Vec<Track>  = Vec::new();

        let division = TimeDivision::from_u16(raw_division);

        let mut offset: usize = 14;

        for i in 0..tracks_num as usize {
            
            if &data[offset..offset + 4] == b"MTrk" {

                    offset += 4;

                    let size = u32::from_be_bytes([
                        data[offset],
                        data[offset + 1],
                        data[offset + 2],
                        data[offset + 3],
                    ]);

                    offset += 4;

                    let track_data = data[offset..offset + size as usize].to_vec();
                    
                    offset += size as usize;

                    tracks.push(Track {
                        num: i,
                        size,
                        data: track_data,
                    });

            }
        }

        Self {
            file_type,
            tracks_num,
            division,
            tracks,
        }
    }
}
