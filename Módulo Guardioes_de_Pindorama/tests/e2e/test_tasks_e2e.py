from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def setup_driver():
    # Configura automaticamente o ChromeDriver
    service = Service(ChromeDriverManager().install())

    # Cria o navegador Chrome
    driver = webdriver.Chrome(service=service)

    return driver


def test_create_single_task_e2e():
    driver = setup_driver()

    try:
        # Acessa a aplicação
        driver.get("http://127.0.0.1:5000")

        # Busca o campo de texto
        input_field = driver.find_element(By.ID, "title")

        # Digita uma tarefa
        input_field.send_keys("Tarefa Selenium")

        # Clica no botão
        driver.find_element(By.ID, "submit").click()

        # Espera a tarefa aparecer na tela
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element(
                (By.ID, "tasks"),
                "Tarefa Selenium",
            )
        )

        # Verifica se a tarefa apareceu
        assert "Tarefa Selenium" in driver.page_source

    finally:
        driver.quit()


def test_create_multiple_tasks_e2e():
    driver = setup_driver()

    try:
        driver.get("http://127.0.0.1:5000")

        input_field = driver.find_element(By.ID, "title")

        # Primeira tarefa
        input_field.send_keys("Tarefa A")
        driver.find_element(By.ID, "submit").click()

        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element(
                (By.ID, "tasks"),
                "Tarefa A",
            )
        )

        # Segunda tarefa
        input_field = driver.find_element(By.ID, "title")

        input_field.send_keys("Tarefa B")
        driver.find_element(By.ID, "submit").click()

        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element(
                (By.ID, "tasks"),
                "Tarefa B",
            )
        )

        # Verifica ambas na tela
        assert "Tarefa A" in driver.page_source
        assert "Tarefa B" in driver.page_source

    finally:
        driver.quit()
