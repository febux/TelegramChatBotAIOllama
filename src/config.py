from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.chat_action import ChatActionMiddleware
from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    bot_token: SecretStr

    ollama_endpoint: str
    ollama_model: str

    messages_limit: int
    # ollama options
    num_keep: int | None = 5
    seed: int | None = 42
    num_predict: int | None = 128
    top_k: int | None = 50
    top_p: float | None = 0.85
    min_p: float | None = 0.0
    tfs_z: float | None = 2.5
    typical_p: float | None = 0.7
    repeat_last_n: int | None = 33
    temperature: float | None = 0.9
    repeat_penalty: float | None = 1.2
    presence_penalty: float | None = 1.5
    frequency_penalty: float | None = 1.2
    mirostat: int | None = 1
    mirostat_tau: float | None = 2.5
    mirostat_eta: float | None = 0.6
    stop: list | None = ["\n", "user:"]
    num_ctx: int | None = 2048
    num_batch: int | None = 2
    num_gpu: int | None = 1
    main_gpu: int | None = 0
    low_vram: bool | None = False
    vocab_only: bool | None = False
    use_mmap: bool | None = True
    use_mlock: bool | None = False
    num_thread: int | None = 8

    mongodb_endpoint: str
    mongodb_port: int
    mongodb_admin_login: str
    mongodb_admin_password: str

    debug: bool = False

    @property
    def ollama_config(self):
        return {
            "model": self.ollama_model,
            "keep_alive": "5m",
            "options": {
                "num_keep": self.num_keep,
                "seed": self.seed,
                "num_predict": self.num_predict,
                "top_k": self.top_k,
                "top_p": self.top_p,
                "min_p": self.min_p,
                "tfs_z": self.tfs_z,
                "typical_p": self.typical_p,
                "repeat_last_n": self.repeat_last_n,
                "temperature": self.temperature,
                "repeat_penalty": self.repeat_penalty,
                "presence_penalty": self.presence_penalty,
                "frequency_penalty": self.frequency_penalty,
                "mirostat": self.mirostat,
                "mirostat_tau": self.mirostat_tau,
                "mirostat_eta": self.mirostat_eta,
                "stop": self.stop,
                "num_ctx": self.num_ctx,
                "num_batch": self.num_batch,
                "num_gpu": self.num_gpu,
                "main_gpu": self.main_gpu,
                "low_vram": self.low_vram,
                "vocab_only": self.vocab_only,
                "use_mmap": self.use_mmap,
                "use_mlock": self.use_mlock,
                "num_thread": self.num_thread
            },
            "stream": True,
        }

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra="ignore")


def config_factory() -> Settings:
    """
    Factory function to create a settings object from environment variables.
    """
    return Settings()


def bot_config_factory(config: Settings) -> tuple[Bot, Dispatcher]:
    """
    Factory function to create a bot and dispatcher with given settings.
    """
    storage = MemoryStorage()
    bot = Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )
    dp = Dispatcher(storage=storage)
    dp.message.middleware(ChatActionMiddleware())
    return bot, dp