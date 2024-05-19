package com.alibou.security.law;

import com.alibou.security.common.rsql.SpecificationBuilder;
import com.alibou.security.exception.ResourceNotFoundException;
import com.alibou.security.law.dto.*;
import com.alibou.security.law.entities.Law;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.io.IOException;
import java.util.List;
import java.util.Objects;
import java.util.UUID;

@Service
@RequiredArgsConstructor
@Transactional
public class LawService {
    private final LawRepository lawRepository;

    public void createLaw(LawCreateDto lawCreateDto) throws Exception {
        try {
            String fileName = StringUtils.cleanPath(Objects.requireNonNull(lawCreateDto.getFile().getOriginalFilename()));

            if (fileName.contains("..") || fileName.isBlank()) {
                throw new Exception("Filename contains invalid path sequence " + fileName);
            }
            Law law = new Law(
                    UUID.randomUUID(),
                    lawCreateDto.getName(),
                    lawCreateDto.getNameRu(),
                    lawCreateDto.getNameEn(),
                    lawCreateDto.getLawType(),
                    lawCreateDto.getLink(),
                    lawCreateDto.getFile().getBytes(),
                    lawCreateDto.getFile().getContentType(),
                    fileName
            );
            lawRepository.save(law);
        } catch (Exception e) {
            throw new Exception("Could not save the file " + e);
        }
    }

    public void updateLaw(LawCreateDto lawUpdateDto, UUID id) throws IOException {
        Law law = lawRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Could not find law - " + id));

        law.setBytes(lawUpdateDto.getFile().getBytes());
        law.setFileType(lawUpdateDto.getFile().getContentType());
        law.setFileName(lawUpdateDto.getFile().getOriginalFilename());

        law.setName(lawUpdateDto.getName());
        law.setNameRu(lawUpdateDto.getNameRu());
        law.setNameEn(lawUpdateDto.getNameEn());
        law.setLawType(lawUpdateDto.getLawType());
        law.setLink(lawUpdateDto.getLink());

        lawRepository.save(law);

    }

    public void delete(UUID id) {
        lawRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Could not find law - " + id));
        lawRepository.deleteById(id);
    }

    public Law getFile(String fileId) {
        return lawRepository
                .findById(UUID.fromString(fileId))
                .orElseThrow(() -> new ResourceNotFoundException("Could not find law with id - " + fileId));
    }

    private String uriString(String id) {
        return ServletUriComponentsBuilder.fromCurrentContextPath()
                .path("/api/v1/public/doc/")
                .path(id)
                .toUriString();
    }

    public LawResponseDto getLaw(UUID id) {
        Law law = lawRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Could not find law - " + id));
        return new LawResponseDto(
                law.getId(),
                law.getName(),
                law.getNameRu(),
                law.getNameEn(),
                law.getLawType(),
                law.getLink(),
                uriString(law.getId().toString())
        );
    }

    public List<LawUzDto> getLawUz() {
        List<Law> laws = lawRepository.findAll();

        return laws.stream().map(law -> {
            String uriString = uriString(law.getId().toString());
            return new LawUzDto(
                    law.getId(),
                    law.getName(),
                    law.getLawType(),
                    law.getLink(),
                    uriString
            );
        }).toList();
    }

    public List<LawRuDto> getLawRu() {
        List<Law> laws = lawRepository.findAll();

        return laws.stream().map(law -> {
            String uriString = uriString(law.getId().toString());
            return new LawRuDto(
                    law.getId(),
                    law.getNameRu(),
                    law.getLawType(),
                    law.getLink(),
                    uriString
            );
        }).toList();
    }

    public List<LawEnDto> getLawEn() {
        List<Law> laws = lawRepository.findAll();

        return laws.stream().map(law -> {
            String uriString = uriString(law.getId().toString());
            return new LawEnDto(
                    law.getId(),
                    law.getNameEn(),
                    law.getLawType(),
                    law.getLink(),
                    uriString
            );
        }).toList();
    }
}
