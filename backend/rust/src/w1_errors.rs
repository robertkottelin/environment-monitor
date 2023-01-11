use std::{fmt, io, num};

#[derive(Debug)]
pub enum W1Error {
    Io(io::Error),
    Parse(num::ParseIntError),
    BadSerialConnection,
}

impl From<io::Error> for W1Error {
    fn from(err: io::Error) -> W1Error {
        W1Error::Io(err)
    }
}

impl From<num::ParseIntError> for W1Error {
    fn from(err: num::ParseIntError) -> W1Error {
        W1Error::Parse(err)
    }
}

impl fmt::Display for W1Error {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match *self {
            W1Error::Io(ref err) => write!(f, "I/O error: {}", err),
            W1Error::Parse(ref err) => write!(f, "Parse error: {}", err),
            W1Error::BadSerialConnection => write!(f, "Bad serial connection"),
        }
    }
}
