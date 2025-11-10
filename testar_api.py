"""
Script para testar rapidamente se a API está funcionando
"""
import sys
import os

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def testar_imports():
    print("🧪 Testando imports...")
    
    try:
        from app.database import Base, engine
        print("✅ app.database - OK")
        
        from app.models.user import User
        print("✅ app.models.user - OK")
        
        from app.models.space import Space
        print("✅ app.models.space - OK")
        
        from app.models.booking import Booking
        print("✅ app.models.booking - OK")
        
        from app.main import app
        print("✅ app.main - OK")
        
        print("\n🎉 Todos os imports funcionaram!")
        print("🚀 Tente executar: python run.py")
        
        # Tentar criar tabelas
        print("\n📦 Criando tabelas no banco...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
        
    except ImportError as e:
        print(f"❌ Erro de import: {e}")
        return False
    except Exception as e:
        print(f"⚠️ Outro erro: {e}")
        return False
    
    return True

if __name__ == "__main__":
    testar_imports()