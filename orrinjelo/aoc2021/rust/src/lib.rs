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



py_module_initializer!(pyaoc, initpyaoc, PyInit_pyaoc, |py, m| { 
    m.add(py, "__doc__", "This module is implemented in Rust.")?; 
    m.add(py, "day01_part1", py_fn!(py, day01_part1(val: Vec<u64>)))?; 
    m.add(py, "day01_part2", py_fn!(py, day01_part2(val: Vec<u64>)))?; 
    Ok(()) 
});

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
