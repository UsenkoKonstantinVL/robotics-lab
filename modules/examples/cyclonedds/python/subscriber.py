#!/usr/bin/env python3
"""Receive example messages with Cyclone DDS Python."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from cyclonedds.domain import DomainParticipant
from cyclonedds.sub import DataReader
from cyclonedds.topic import Topic
from cyclonedds.util import duration
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
    reader = DataReader(participant, topic)

    received_count = 0
    for message in reader.take_iter(timeout=duration(seconds=10)):
        print(
            f'received sequence={message.sequence_number} sender={message.sender} '
            f'text="{message.text}"',
            flush=True,
        )
        received_count += 1
        if received_count == args.count:
            return 0

    print(
        f"subscriber timed out after receiving {received_count} of {args.count} messages"
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
