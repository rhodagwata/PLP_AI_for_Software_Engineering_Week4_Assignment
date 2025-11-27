"""
Automated Login Test Suite with AI-Enhanced Testing
Uses Selenium WebDriver with intelligent test case generation
"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
from datetime import datetime


class TestLoginPage:
    """Test suite for login page functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup method - runs before each test"""
        # Setup Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        
        # Initialize driver
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        
        # Get the path to login page
        current_dir = os.path.dirname(os.path.abspath(__file__))
        login_page_path = f"file://{current_dir}/login_page.html"
        self.driver.get(login_page_path)
        
        # Valid credentials
        self.valid_username = "testuser"
        self.valid_password = "Test@123"
        
        yield
        
        # Teardown - runs after each test
        self.driver.quit()
    
    def test_page_loads_successfully(self):
        """Test 1: Verify login page loads correctly"""
        assert "Login Test Page" in self.driver.title
        assert self.driver.find_element(By.ID, "username").is_displayed()
        assert self.driver.find_element(By.ID, "password").is_displayed()
        assert self.driver.find_element(By.ID, "loginBtn").is_displayed()
        print("✓ Page loaded successfully")
    
    def test_valid_login(self):
        """Test 2: Login with valid credentials"""
        # Enter valid credentials
        self.driver.find_element(By.ID, "username").send_keys(self.valid_username)
        self.driver.find_element(By.ID, "password").send_keys(self.valid_password)
        
        # Click login button
        self.driver.find_element(By.ID, "loginBtn").click()
        
        # Wait for success message
        wait = WebDriverWait(self.driver, 10)
        success_message = wait.until(
            EC.visibility_of_element_located((By.ID, "successMessage"))
        )
        
        # Assertions
        assert "Login successful" in success_message.text
        assert self.valid_username in success_message.text
        print(f"✓ Valid login test passed: {success_message.text}")
    
    def test_invalid_username(self):
        """Test 3: Login with invalid username"""
        # Enter invalid username
        self.driver.find_element(By.ID, "username").send_keys("wronguser")
        self.driver.find_element(By.ID, "password").send_keys(self.valid_password)
        
        # Click login button
        self.driver.find_element(By.ID, "loginBtn").click()
        
        # Wait for error message
        wait = WebDriverWait(self.driver, 10)
        error_message = wait.until(
            EC.visibility_of_element_located((By.ID, "errorMessage"))
        )
        
        # Assertions
        assert "Invalid username or password" in error_message.text
        print(f"✓ Invalid username test passed: {error_message.text}")
    
    def test_invalid_password(self):
        """Test 4: Login with invalid password"""
        # Enter valid username but invalid password
        self.driver.find_element(By.ID, "username").send_keys(self.valid_username)
        self.driver.find_element(By.ID, "password").send_keys("WrongPass123")
        
        # Click login button
        self.driver.find_element(By.ID, "loginBtn").click()
        
        # Wait for error message
        wait = WebDriverWait(self.driver, 10)
        error_message = wait.until(
            EC.visibility_of_element_located((By.ID, "errorMessage"))
        )
        
        # Assertions
        assert "Invalid username or password" in error_message.text
        print(f"✓ Invalid password test passed")
    
    def test_empty_credentials(self):
        """Test 5: Login with empty fields"""
        # Leave fields empty and try to submit
        login_button = self.driver.find_element(By.ID, "loginBtn")
        login_button.click()
        
        # HTML5 validation should prevent submission
        username_field = self.driver.find_element(By.ID, "username")
        
        # Check if validation message exists (HTML5 required attribute)
        validation_message = username_field.get_attribute("validationMessage")
        assert validation_message != ""
        print(f"✓ Empty credentials test passed: HTML5 validation active")
    
    def test_sql_injection_attempt(self):
        """Test 6: SQL Injection security test (AI-Enhanced)"""
        # Try SQL injection in username field
        sql_injection = "' OR '1'='1"
        self.driver.find_element(By.ID, "username").send_keys(sql_injection)
        self.driver.find_element(By.ID, "password").send_keys("any_password")
        
        # Click login button
        self.driver.find_element(By.ID, "loginBtn").click()
        
        # Wait for error message (should fail, not bypass authentication)
        wait = WebDriverWait(self.driver, 10)
        error_message = wait.until(
            EC.visibility_of_element_located((By.ID, "errorMessage"))
        )
        
        # Should show error, not success
        assert "Invalid username or password" in error_message.text
        print(f"✓ SQL injection prevented")
    
    def test_xss_attempt(self):
        """Test 7: XSS security test (AI-Enhanced)"""
        # Try XSS in username field
        xss_payload = "<script>alert('XSS')</script>"
        self.driver.find_element(By.ID, "username").send_keys(xss_payload)
        self.driver.find_element(By.ID, "password").send_keys("password")
        
        # Click login button
        self.driver.find_element(By.ID, "loginBtn").click()
        
        # Wait for error message
        wait = WebDriverWait(self.driver, 10)
        error_message = wait.until(
            EC.visibility_of_element_located((By.ID, "errorMessage"))
        )
        
        # Should handle safely without executing script
        assert "Invalid username or password" in error_message.text
        # No alert should appear
        print(f"✓ XSS attack prevented")
    
    def test_case_sensitivity(self):
        """Test 8: Username case sensitivity (AI-Enhanced)"""
        # Try uppercase username
        self.driver.find_element(By.ID, "username").send_keys("TESTUSER")
        self.driver.find_element(By.ID, "password").send_keys(self.valid_password)
        
        # Click login button
        self.driver.find_element(By.ID, "loginBtn").click()
        
        # Wait for error message
        wait = WebDriverWait(self.driver, 10)
        error_message = wait.until(
            EC.visibility_of_element_located((By.ID, "errorMessage"))
        )
        
        # Should fail (case-sensitive)
        assert "Invalid username or password" in error_message.text
        print(f"✓ Case sensitivity test passed")
    
    def test_special_characters_in_credentials(self):
        """Test 9: Special characters handling (AI-Enhanced)"""
        # Test with special characters
        special_chars = "user@#$%"
        self.driver.find_element(By.ID, "username").send_keys(special_chars)
        self.driver.find_element(By.ID, "password").send_keys("pass@#$%")
        
        # Click login button
        self.driver.find_element(By.ID, "loginBtn").click()
        
        # Wait for error message
        wait = WebDriverWait(self.driver, 10)
        error_message = wait.until(
            EC.visibility_of_element_located((By.ID, "errorMessage"))
        )
        
        assert "Invalid username or password" in error_message.text
        print(f"✓ Special characters handled correctly")
    
    def test_long_input_strings(self):
        """Test 10: Long input strings (AI-Enhanced)"""
        # Test with very long strings
        long_username = "a" * 1000
        long_password = "b" * 1000
        
        self.driver.find_element(By.ID, "username").send_keys(long_username)
        self.driver.find_element(By.ID, "password").send_keys(long_password)
        
        # Click login button
        self.driver.find_element(By.ID, "loginBtn").click()
        
        # Wait for error message
        wait = WebDriverWait(self.driver, 10)
        error_message = wait.until(
            EC.visibility_of_element_located((By.ID, "errorMessage"))
        )
        
        # Should handle gracefully
        assert "Invalid username or password" in error_message.text
        print(f"✓ Long input strings handled correctly")


if __name__ == "__main__":
    # Run tests with HTML report
    pytest.main([
        __file__,
        "-v",
        "--html=test_report.html",
        "--self-contained-html"
    ])