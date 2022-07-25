import kserve
from torchvision import models, transforms
from typing import Dict
import torch
from PIL import Image
import base64
import io


class AlexNetModel(kserve.KFModel):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.ready = False

    def load(self):
        model = models.AlexNet()
        model.load_state_dict(torch.load('/mnt/models/alexnet-owt-7be5be79.pth'))
        model.eval()
        self.model = model
        self.ready = True

    def predict(self, request: Dict) -> Dict:
        inputs = request["instances"]

        # Input follows the Tensorflow V1 HTTP API for binary values
        # https://www.tensorflow.org/tfx/serving/api_rest#encoding_binary_values
        data = inputs[0]["image"]["b64"]

        raw_img_data = base64.b64decode(data)
        input_image = Image.open(io.BytesIO(raw_img_data))

        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])

        input_tensor = preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0)

        output = self.model(input_batch)

        probabilities = torch.nn.functional.softmax(output[0], dim=0)

        with open("/model-server/imagenet_classes.txt", "r") as f:
            categories = [s.strip() for s in f.readlines()]

        top5_prob, top5_catid = torch.topk(probabilities, 5)
        
        result = {}
        for i in range(top5_prob.size(0)):
            result[categories[top5_catid[i]]] = top5_prob[i].item()

        return result


if __name__ == "__main__":
    model = AlexNetModel("alexnet-model")
    model.load()
    kserve.KFServer(workers=1).start([model])