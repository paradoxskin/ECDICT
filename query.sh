#!/bin/bash
once() {
    echo $1 > /tmp/stardict.r.fifo
    cat /tmp/stardict.w.fifo
}

if [[ "$1" == "-i" ]]; then
    while [[ not_the_end_of_the_world ]]; do
        read -e -p "> " question
        once "$question"
    done
fi
