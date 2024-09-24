const fs = require('fs');
const path = require('path');

// Define the current directory
const currentDirectory = __dirname;

// Function to extract unique brand names from all JSON files in the directory
function extractUniqueBrandNames() {
    try {
        const brandNames = new Set(); // Use a Set to store unique brand names
        // Read all files in the directory
        const files = fs.readdirSync(currentDirectory);
        console.log(files)
        // Loop through each file
        files.forEach(file => {
            if (path.extname(file) === '.json') { // Check if file is JSON
                // Read the JSON file
                const data = JSON.parse(fs.readFileSync(path.join(currentDirectory, file)));
                // Extract brand names from the data
                data.forEach(item => {
                    if (item.brand) {
                        brandNames.add(item.brand);
                    }
                });
            }
        });
                fs.writeFileSync(path.join(currentDirectory,'brands.txt'), JSON.stringify(Array.from(brandNames)), err => {
  if (err) {
    console.error(err);
  } else {
    // file written successfully
  }
});
        // Convert the Set to an array and return
        // return Array.from(brandNames);
    } catch (error) {
        console.error('Error extracting unique brand names:', error);
        return { error: 'Internal Server Error' };
    }
}

// Function to extract all products from JSON files in the directory
function extractAllProducts() {
    try {
        const products = []; // Use an array to store all products
        // Read all files in the directory
        const files = fs.readdirSync(currentDirectory);
        // Loop through each file
        files.forEach(file => {
            if (path.extname(file) === '.json') { // Check if file is JSON
                // Read the JSON file
                const data = JSON.parse(fs.readFileSync(path.join(currentDirectory, file)));
                // Add each product to the array
                data.forEach(item => {
                    products.push(item);
                });
            }
        });

        return products;
    } catch (error) {
        console.error('Error extracting all products:', error);
        return { error: 'Internal Server Error' };
    }
}

// Function to get a random product from all JSON files in the directory
function getRandomProduct() {
const random = []
    try {
        const products = extractAllProducts();
        if (products.length === 0) {
            return { error: 'No products found' };
        }
        for(let i =0; i<10; i++){
        const randomIndex = Math.floor(Math.random() * products.length);
         random.push(products[randomIndex]);

        }
        return random
    } catch (error) {
        console.error('Error getting random product:', error);
        return { error: 'Internal Server Error' };
    }
}

console.log(extractUniqueBrandNames());
// console.log(getRandomProduct());

// Export functions
module.exports = { extractUniqueBrandNames, getRandomProduct };

