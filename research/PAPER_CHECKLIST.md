# Primary-source reading checklist

Use this as a **whiteboard prep** list for on-camera beats and interview Q&A. Tina works through it manually; nothing here auto-validates completion.

| Priority | Paper / source | What to internalize |
| -------- | ---------------- | ------------------- |
| P0 | Kaplan et al., *Scaling Laws for Neural Language Models* (2020), arXiv:2001.08361 | Power-law loss vs params/data/compute; equation form L(N). |
| P0 | Hoffmann et al., *Training Compute-Optimal Large Language Models* (Chinchilla, 2022), arXiv:2203.15556 | Isoflops argument; ~20 tokens/param rule of thumb. |
| P0 | Vaswani et al., *Attention Is All You Need* (2017), arXiv:1706.03762 | QKV construction; softmax(QKᵀ/√d)V; why n×n is unavoidable in dense attention. |
| P1 | Dao et al., FlashAttention (1 / 2 / 3 on arXiv) | IO-bound story; tiling; asymptotic still O(n²). |
| P1 | Gu & Dao, *Mamba* (2023), arXiv:2312.00752 | Selective SSM intuition; linear-time recurrence vs attention grid. |
| P1 | Poli et al., *Hyena Hierarchy* (2023), arXiv:2302.10866 | Long conv / FFT path; where O(n log n) enters. |
| P2 | Survey / blog on linear attention (Performer, RetNet, etc.) | Kernel trick / ϕ(Q)ϕ(K)ᵀ reordering. |
| P2 | Hybrid architectures (SAMBA, Jamba, Griffin — pick one paper each) | Why people interleave attention + subquadratic blocks. |

**SubQ product facts** (not peer-reviewed): summarize from [Introducing SubQ](https://subq.ai/introducing-subq) with dates and hedge language — numbers are SubQ-reported until replicated.
