"""Copyright 2024 Tanner Corcoran

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

__author__ = "Tanner Corcoran"
__license__ = "Apache 2.0 License"
__copyright__ = "Copyright (c) 2024 Tanner Corcoran"


import re
import csv
import sys
import copy
import enum
import pathlib
import datetime
from typing import *

from _base import (
    MCC,
    ISOCC,
    City,
    Status,
    MICEntry,
)


PD = pathlib.Path(__file__).parent
_T = TypeVar("_T")


class Parser:
    """Parses the MIC sheet
    (https://www.iso20022.org/market-identifier-codes) into `MICEntry`
    instances.

    """
    hyphen_re = re.compile(
        r"[\u002D\u058A\u05BE\u1400\u1806\u2010-\u2015\u2E17\u2E1A\u2E3A"
        r"\u2E3B\u2E40\u301C\u3030\u30A0\uFE31\uFE32\uFE58\uFE63\uFF0D]"
    )
    ws_re = re.compile(r"\s+")

    @staticmethod
    def _parse_date(datestr: str) -> datetime.date:
        return datetime.date(
            year=int(datestr[:4]),
            month=int(datestr[4:6]),
            day=int(datestr[6:])
        )

    @classmethod
    def _normalize(cls, value: str) -> str:
        return re.sub(cls.hyphen_re, "-", re.sub(cls.ws_re, " ", value))

    @staticmethod
    def _parse_icc(icc: str) -> ISOCC:
        if icc in {"in", "is"}:
            icc += "_"
        return ISOCC[icc]

    @classmethod
    def parse(
        cls, csv_src: pathlib.Path
    ) -> Tuple[MICEntry, ...]:
        mics: Dict[str, MICEntry] = dict()

        with csv_src.open("r") as infile:
            reader = csv.reader(infile.readlines())
            next(reader) # skip header
            lines: List[Tuple[str, ...]] = list(reader)

        while lines:
            for entry in copy.deepcopy(lines):
                (
                    mic,
                    op_mic,
                    _,
                    mname_and_inst_desc,
                    le_name,
                    le_id,
                    mcc,
                    anym,
                    icc,
                    city,
                    website,
                    status,
                    c_date,
                    lu_date,
                    lv_date,
                    e_date,
                    comments,
                ) = entry

                if mic != op_mic and op_mic.lower() not in mics:
                    continue

                mname, inst_desc, *_ = (
                    *re.split(r" - ", mname_and_inst_desc, maxsplit=1),
                    None,
                )

                mics[mic.lower()] = MICEntry(
                    mic=mic,
                    market_name=cls._normalize(mname),
                    market_category_code=MCC[mcc.lower()],
                    creation_date=cls._parse_date(c_date),
                    status=Status[status.lower()],
                    city=(
                        City(cls._normalize(city).title())
                        if city and city != "N/A" else None
                    ),
                    operating_mic=(
                        mics[op_mic.lower()] if mic != op_mic else None
                    ),
                    institution_description=inst_desc,
                    legel_entity_name=(le_name or None),
                    legal_entity_identifier=(le_id or None),
                    acronym=(anym or None),
                    iso_country_code=(
                        cls._parse_icc(icc.lower()) if icc else None
                    ),
                    website=(website.lower() or None),
                    last_update_date=(
                        cls._parse_date(lu_date) if lu_date else None
                    ),
                    last_validation_date=(
                        cls._parse_date(lv_date) if lv_date else None
                    ),
                    expiry_date=(
                        cls._parse_date(e_date) if e_date else None
                    ),
                    comments=(comments or None)
                )
                lines.remove(entry)
        
        return tuple(mics.values())


class Serializer:
    @staticmethod
    def _o(
        value: Union[_T, None], serializer: Callable[..., bytes], *args: Any
    ) -> bytes:
        if value is None:
            return bytes((0,))

        b = bytes((1,))
        return b + serializer(value, *args)

    @staticmethod
    def _s(value: str, size: int) -> bytes:
        encoded = value.encode("utf-8")
        length = len(encoded).to_bytes(size or 2, "big")
        return length + encoded

    @staticmethod
    def _d(value: datetime.date) -> bytes:
        # year       : 15
        # month      : 4
        # day        : 5
        return (
            (value.year << 9)
            | (value.month << 5)
            | value.day
        ).to_bytes(3, "big")

    @staticmethod
    def _e(value: enum.Enum, size: int) -> bytes:
        return int(value.value).to_bytes(size, "big")

    @classmethod
    def serialize(cls, e: MICEntry) -> bytes:
        def gen() -> Generator[bytes, None, None]:
            yield cls._s(e.mic, 1)
            yield cls._s(e.market_name, 1)
            yield cls._e(e.market_category_code, 1)
            yield cls._d(e.creation_date)
            yield cls._e(e.status, 1)
            yield cls._o(e.city, cls._e, 2)
            yield cls._o((e.operating_mic and e.operating_mic.mic), cls._s, 1)
            yield cls._o(e.institution_description, cls._s, 1)
            yield cls._o(e.legel_entity_name, cls._s, 1)
            yield cls._o(e.legal_entity_identifier, cls._s, 1)
            yield cls._o(e.acronym, cls._s, 1)
            yield cls._o(e.iso_country_code, cls._e, 1)
            yield cls._o(e.website, cls._s, 1)
            yield cls._o(e.last_update_date, cls._d)
            yield cls._o(e.last_validation_date, cls._d)
            yield cls._o(e.expiry_date, cls._d)
            yield cls._o(e.comments, cls._s, 2)

        return b"".join(gen())


def build(mics: Sequence[MICEntry]) -> None:
    def format_mic(mic: str) -> str:
        mic = mic.lower()
        if (
            mic[0].isdigit()
            or mic in {"else", "from", "pass", "with"}
        ):
            return f"_{mic}"
        return mic

    # create the source file
    with (PD / "src" / "iso10383" / "_iso10383.py").open("w") as outfile:
        # base file
        with (PD / "_base.py").open("r") as infile:
            outfile.write(infile.read().strip())

        # enum contents
        for e in mics:
            outfile.write(f"\n    {format_mic(e.mic)} = None")
        outfile.write("\n\n\n")

        # deserializer
        with (PD / "_deserializer.txt").open("r") as infile:
            outfile.write(infile.read().strip())

        # final newline
        outfile.write("\n")

    # serialize mics
    with (PD / "src" / "iso10383" / "_data").open("wb") as outfile:
        outfile.write(len(mics).to_bytes(2, "big"))
        for e in mics:
            outfile.write(Serializer.serialize(e))


def main() -> None:
    if len(sys.argv) != 2:
        print("Must provide absolute path to ISO_10383 CSV file")
        return

    # get path
    path = pathlib.Path(sys.argv[1])

    # parse csv
    mics = Parser.parse(path)

    # build
    build(mics)


if __name__ == "__main__":
    main()
