package com.password_manager.password_manager.services.utils;

import com.password_manager.password_manager.Repositories.CodeRepository;
import com.password_manager.password_manager.enums.CodeContextEnum;
import com.password_manager.password_manager.enums.CodeStatsEnum;
import com.password_manager.password_manager.models.CodeModel;
import com.password_manager.password_manager.models.UserModel;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Random;

@Component
public class CodeUtils {

    @Autowired
    private CodeRepository codeRepository;

    public boolean existSomeCode(UserModel userModel) {
        return this.codeRepository.findByUserModel(userModel.getId()).isEmpty();
    }

    public boolean verifyCode(String code) {
        return this.codeRepository.findByCode(code).isPresent();
    }

    public CodeModel createCode(UserModel userModel, CodeContextEnum context) {
        this.invalidateAnotherCodes(userModel);
        CodeModel codeModel = new CodeModel();
        codeModel.setUserModel(userModel);
        codeModel.setCode(this.generateCode());
        codeModel.setContext(context);
        codeModel.setStats(CodeStatsEnum.ENABLED);
        return codeModel;
    }

    public String generateCode() {
        Random random = new Random();
        String code = String.valueOf(random.nextInt(1000, 9999));
        if (verifyCode(code)) {
            this.generateCode();
        }
        return code;
    }

    public void invalidateAnotherCodes(UserModel userModel) {
        if (!this.existSomeCode(userModel)) {
            List<CodeModel> codeModelList = this.codeRepository.findByUserModel(userModel.getId());
            codeModelList.forEach(code -> code.setStats(CodeStatsEnum.DISABLED));
        }
    }

}
