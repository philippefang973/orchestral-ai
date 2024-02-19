if command -v python &> /dev/null; then
    echo "OK python is installed"
else 
    echo "python is required to run"
fi

if command -v pip &> /dev/null; then
    echo "OK pip is installed"
else 
    echo "pip is required to run"
fi

if command -v docker &> /dev/null; then
    echo "OK docker is installed"
else 
    echo "docker is required to run"
fi

if command -v npm &> /dev/null; then
    echo "OK npm is installed"
else 
    echo "npm is required to run"
fi

if command -v kubectl &> /dev/null; then
    echo "OK kubectl is installed"
else 
    echo "kubectl is required to run"
fi

if command -v minikube &> /dev/null; then
    echo "OK minikube is installed"
else 
    echo "minikube is required to run"
fi