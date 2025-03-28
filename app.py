import streamlit as st
from PIL import Image
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import torch.nn.functional as F

# Define the mapping of class names to bins
bin_map = {
    "water bottle": "Recycling",
    "plastic bag": "Garbage",
    "banana": "Compost",
    "apple": "Compost",
    "pizza": "Compost",
    "paper towel": "Compost",
    "newspaper": "Recycling",
    "can": "Recycling",
    "coffee cup": "Garbage",
    "cardboard": "Recycling",
    "glass bottle": "Recycling",
    "food": "Compost"
}

# Load a pre-trained image classification model
model = models.mobilenet_v2(pretrained=True)
model.eval()

# Load ImageNet class labels
LABELS_URL = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
imagenet_classes = [line.strip() for line in torch.hub.load_state_dict_from_url(LABELS_URL, model_dir=".").splitlines()]

# Preprocessing transformation
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

st.set_page_config(page_title="EcoSort", layout="centered")
st.title("🚮 EcoSort: Smart Waste Classifier")
st.write("Upload a photo of your item and I'll tell you which bin it goes in: Recycling, Compost, or Garbage.")

uploaded_file = st.file_uploader("Upload an image of the item", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Preprocess
    img_t = transform(image)
    batch_t = torch.unsqueeze(img_t, 0)

    # Predict
    with torch.no_grad():
        out = model(batch_t)
        probabilities = F.softmax(out[0], dim=0)
        top5 = torch.topk(probabilities, 5)

    st.subheader("Top Predictions")
    for i in range(5):
        class_idx = top5.indices[i].item()
        class_name = imagenet_classes[class_idx]
        score = top5.values[i].item()
        bin_type = bin_map.get(class_name.lower(), "Uncertain")
        st.write(f"**{class_name}** ({score*100:.2f}%) → **{bin_type}**")

    st.success("Hope this helps you sort smarter! 🚚")
