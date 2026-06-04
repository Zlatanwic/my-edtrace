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
    两个Gap()
    SAS的贡献()
    System_Overview()


def kv_cache():
    text("kv cache在一定程度上解决了decode阶段的compute-bound问题，就是避免每次decode都需要重新算一遍历史token的kv，但是又占用了大量显存")


def sparse_attention():
    text("## sparse attention")
    text("模型不需要每次都attend所有历史token，而是“稀疏”地attend部分token,省计算+省内存")
    text("### 静态稀疏vs动态稀疏")
    text("- 静态：根据位置决定attend哪些token，比如sliding window，strided attention")
    image("../../images/static.png", width=700)
    text("- 动态：根据运行时内容决定看哪些 token，做importance score(H2O)")
    image("../../images/dyn.png", width=400)

def 两个Gap():
    text("### Gap1:Programming abstraction 不够好")
    text("sparse attention算法设计很快，但是系统实现困难。很多都是写死的，一个新的sprase pattern较难迁移")
    text("### Gap2:KV cache 优化不自动")
    text("SAS要自动推导三项：")
    text("1. 最小 KV cache size 是多少？")
    text("2. 当前 query 应该看 cache 里的哪些 entry？")
    text("3. 新 token 的 KV 应该写入 cache 的哪个位置？")

def SAS的贡献():
    text("第一，SAS 是一个同时支持静态和动态 sparse attention 的自动 kernel 生成工具。")
    text("第二，SAS 提供一种 DSL / programming abstraction，让用户用 primitive 和逻辑操作符组合 attention pattern。")
    text("第三，SAS 有一个几何分析器，可以从 attention pattern 中提取规律，自动生成 KV cache 管理函数。")
    text("第四，SAS 支持 Nvidia GPU 和 AWS Trainium 两个后端，不只是单硬件上的 prototype。")
    text("实验上，SAS 在 GPU 上相对 FlexAttention 的 context encoding 有 1.10–1.22× speedup，token generation 有 2.68–2.80× speedup；在 Trainium 上相对 dense attention 也有明显加速。")


def System_Overview():
    image("../../images/sas_overview.png", width=700)
    text("```python\np = Diag(size=2)\np += Dynamic(budget=2, score=sas.op.attn_score.sum(dim=1))\n```")
