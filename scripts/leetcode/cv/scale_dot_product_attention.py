
import torch

import torch.nn as nn

import torch.nn.functional as F

import numpy as np



class ScaleDotProductAttention(nn.Module):
    def __init__(self, scale):
        super().__init__()
        self.scale = scale
        self.softmax = nn.Softmax(dim=2)
        
    def forward(self, q, k, v, mask=None):
        u = torch.bmm(q, k.transpose(1, 2)) / self.scale
        
        if mask is not None:
            u = u.masked_fill(mask, -np.inf)
            
        attn = self.softmax(u)
        
        output = torch.bmm(attn, v)
        
        return attn, output
    
    
if __name__ == "__main__":
    batch = 3
    n_q, n_k, n_v = 2, 4, 4
    d_q, d_k, d_v = 128, 128, 54
    
    q = torch.randn(batch, n_q, d_q)
    k = torch.randn(batch, n_k, d_k)
    v = torch.randn(batch, n_v, d_v)
    mask = torch.zeros(batch, n_q, n_k).bool()
    
    