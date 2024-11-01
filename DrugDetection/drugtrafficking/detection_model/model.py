import torch

class ContentDetectionModel:
    def __init__(self, model_path):
        self.model = self.load_model(model_path)

    def load_model(self, model_path):
        """Load the model weights from the specified path."""
        model = torch.load(model_path, map_location=torch.device('cpu'))  # Adjust as needed for your setup
        model.eval()  # Set the model to evaluation mode
        return model

    def predict(self, input_data):
        """Make predictions using the loaded model."""
        with torch.no_grad():
            output = self.model(input_data)  # Adjust input_data preprocessing as needed
        return output
