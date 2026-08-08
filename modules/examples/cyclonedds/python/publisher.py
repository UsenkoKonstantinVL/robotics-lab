#!/usr/bin/env python3
"""Publish example messages with Cyclone DDS Python."""

from __future__ import annotations

import argparse
import time
from collections.abc import Sequence

from cyclonedds.domain import DomainParticipant
from cyclonedds.pub import DataWriter
from cyclonedds.topic import Topic
from robotics_lab_examples import HelloMessage


TOPIC_NAME = "robotics_lab.examples.hello"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("count", nargs="?", type=int, default=5)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    participant = DomainParticipant()
    topic = Topic(participant, TOPIC_NAME, HelloMessage)
    writer = DataWriter(participant, topic)

    time.sleep(1)
    for sequence_number in range(1, args.count + 1):
        message = HelloMessage(
            sender="python-publisher",
            sequence_number=sequence_number,
            text="Hello from Cyclone DDS Python",
        )
        writer.write(message)
        print(
            f"published sequence={message.sequence_number} "
            f"sender={message.sender}",
            flush=True,
        )
        time.sleep(0.2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
