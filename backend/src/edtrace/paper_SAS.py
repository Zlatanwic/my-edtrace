import numpy as np
import torch
from dataclasses import dataclass
from .execute_util import text, image, link, plot, note

def main():
    in_one_word()
    背景介绍()








def in_one_word():
    text("简单来说，SAS主要是一个sparse attention编译器/生成器，从用户的简单的几句代码，生成高性能kernel")

def 背景介绍():
    kv_cache()
    sparse_attention()


def kv_cache():
    text("kv cache在一定程度上解决了decode阶段的compute-bound问题，就是避免每次decode都需要重新算一遍历史token的kv，但是又占用了大量显存")


def sparse_attention():
    text("## sparse attention")
    text("模型不需要每次都attend所有历史token，而是“稀疏”地attend部分token,省计算+省内存")
    text("### 静态稀疏vs动态稀疏")
    text("- 静态：根据位置决定attend哪些token")
    image("../../images/static.png", width=200)
    text("- 动态：根据运行时内容决定看哪些 token")
