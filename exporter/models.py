from dataclasses import dataclass


@dataclass
class DatabaseSettings:
    user: str
    password: str
    host: str
    port: int
    database: str


@dataclass
class Result:
    sport_pass_id: str
    first_name: str
    last_name: str
    club: str
    club_id: str
    starter_list: str
    starter_list_id: str
    start_number: str
    target_number: str
    discipline: str
    ranking: str
    series1: int
    series2: int
    series3: int
    inner_tens: int
    total: int

    @property
    def full_name(self) -> str:
        return f"{self.last_name} - {self.first_name}"

    @property
    def rounded_total(self) -> int:
        return round(self.total/10)
