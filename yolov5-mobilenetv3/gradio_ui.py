import torch
import gradio as gr


def detect_fall(img, conf, iou):
    model.conf = conf
    model.iou = iou
    return model(img).render()[0]


model = torch.hub.load('./', "custom", path='fall.pt', source='local')
title = "人体跌倒检测系统"
description = "人体跌倒检测系统"
base_conf, base_iou = 0.25, 0.45


gr.Interface(fn=detect_fall, inputs=["image", gr.Slider(0, 1.0, value=base_conf), gr.Slider(0, 1.0, value=base_iou)], 
             outputs=["image"],
             live=True,
             title=title, 
             description=description, 
             examples=[["./datasets/images/val/people(138).jpg", base_conf, base_iou], ["./datasets/images/val/people(273).jpg", base_conf, base_iou]],
            ).launch()