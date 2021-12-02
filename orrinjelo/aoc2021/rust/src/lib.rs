#[macro_use]
extern crate cpython;

use cpython::{PyResult, Python};

fn day01_part1(_py: Python, vals: Vec<u64>) -> PyResult<u64> {
    let mut count = 0;
    let mut last = 0;
    for x in vals {
        if last != 0 && last < x {
            count += 1;
        }
        last = x;
    }

    Ok(count)
}


fn day01_part2(_py: Python, vals: Vec<u64>) -> PyResult<u64> {
    let mut count = 0;
    let mut last = 0;
    for i in 0..vals.len()-2 {
        if last != 0 && last < vals[i]+vals[i+1]+vals[i+2] {
            count += 1;
        }
        last = vals[i]+vals[i+1]+vals[i+2];
    }

    Ok(count)
}

fn day02_part1(_py: Python, instructions: Vec<String>) -> PyResult<u64> {
    let mut posx: u64 = 0;
    let mut posy: u64 = 0;

    for line in instructions {
        let split = line.split_whitespace().collect::<Vec<&str>>();
        let dir = split[0];
        let dist: u64 = split[1].parse().unwrap();

        match dir {
            "forward" => {
                posx += dist;
            },
            "up" => {
                posy -= dist;
            },
            "down" => {
                posy += dist;
            },
            _ => {
            }
        }
    }

    Ok(posx * posy)
}

fn day02_part2(_py: Python, instructions: Vec<String>) -> PyResult<u64> {
    let mut posx: u64 = 0;
    let mut posy: u64 = 0;
    let mut aim: u64 = 0;

    for line in instructions {
        let split = line.split_whitespace().collect::<Vec<&str>>();
        let dir = split[0];
        let dist: u64 = split[1].parse().unwrap();

        match dir {
            "forward" => {
                posx += dist;
                posy += dist*aim;
            },
            "up" => {
                aim -= dist;
            },
            "down" => {
                aim += dist;
            },
            _ => {
            }
        }
    }

    Ok(posx * posy)
}

py_module_initializer!(pyaoc, initpyaoc, PyInit_pyaoc, |py, m| { 
    m.add(py, "__doc__", "This module is implemented in Rust.")?; 
    m.add(py, "day01_part1", py_fn!(py, day01_part1(val: Vec<u64>)))?; 
    m.add(py, "day01_part2", py_fn!(py, day01_part2(val: Vec<u64>)))?; 
    m.add(py, "day02_part1", py_fn!(py, day02_part1(val: Vec<String>)))?; 
    m.add(py, "day02_part2", py_fn!(py, day02_part2(val: Vec<String>)))?; 
    Ok(()) 
});

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
