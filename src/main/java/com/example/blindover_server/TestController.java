package com.example.blindover_server;
import lombok.extern.slf4j.Slf4j;
import org.pytorch.IValue;
import org.pytorch.Tensor;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;
import org.pytorch.Module;
import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.io.InputStream;
import java.util.Arrays;

@Slf4j
@Controller
public class TestController {

    private static final int IMG_WIDTH = 224;
    private static final int IMG_HEIGHT = 224;
    @PostMapping("")
    public String uploadImage(@RequestParam("image") MultipartFile image) {
        try {

            // 이미지를 Tensor로 변환
            try (InputStream is = getClass().getResourceAsStream("/shufflenet_wesight.pt")) {
                log.info("진짜 좀 되라 시");
            } catch (IOException e) {
                throw new RuntimeException("모델 파일을 불러올 수 없습니다.", e);
            }

            BufferedImage bufferedImage = ImageIO.read(image.getInputStream());
            BufferedImage resizedImage = resizeImage(bufferedImage); // 이미지 크기 조정
            float[] inputData = normalizeImage(resizedImage); // 이미지 정규화
            Tensor inputTensor = Tensor.fromBlob(inputData, new long[]{1, 3, 224, 224});

            // 모델 로드
            Module module = Module.load("shufflenet_weight.pt");


            // 모델에 입력 전달하여 예측 수행
            IValue output = module.forward(IValue.from(inputTensor));
            Tensor outputTensor = output.toTensor();

            // 예측 결과 출력
            float[] outputData = outputTensor.getDataAsFloatArray();
            System.out.println("Prediction: " + Arrays.toString(outputData));

            return "Image uploaded and processed successfully";
        } catch (Exception e) {
            e.printStackTrace();
            return "Error processing the uploaded image";
        }
    }

    private BufferedImage resizeImage(BufferedImage image) {
        // 이미지 크기 조정 로직 구현
        // 예: ImageIO 또는 Java Advanced Imaging (JAI) 라이브러리 활용
        Image resizedImage = image.getScaledInstance(IMG_WIDTH, IMG_HEIGHT, Image.SCALE_DEFAULT);

        BufferedImage bufferedResizedImage = new BufferedImage(IMG_WIDTH, IMG_HEIGHT, BufferedImage.TYPE_INT_RGB);
        Graphics2D g2d = bufferedResizedImage.createGraphics();
        g2d.drawImage(resizedImage, 0, 0, null);
        g2d.dispose();

        return bufferedResizedImage;
    }


    private float[] normalizeImage(BufferedImage image) {
        int width = image.getWidth();
        int height = image.getHeight();
        int channels = 3; // RGB 이미지의 경우 3개의 채널 (Red, Green, Blue)

        float[] normalizedData = new float[width * height * channels];
        int pixelIdx = 0;

        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                Color color = new Color(image.getRGB(x, y));

                // RGB 값을 0에서 1 사이의 값으로 정규화
                float red = color.getRed() / 255.0f;
                float green = color.getGreen() / 255.0f;
                float blue = color.getBlue() / 255.0f;

                // 정규화된 RGB 값을 배열에 저장
                normalizedData[pixelIdx++] = red;
                normalizedData[pixelIdx++] = green;
                normalizedData[pixelIdx++] = blue;
            }
        }

        return normalizedData;
    }

}
