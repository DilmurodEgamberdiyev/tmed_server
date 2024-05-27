package com.alibou.security.about;

import com.alibou.security.about.dto.AboutCreateDto;
import com.alibou.security.about.dto.AboutEnDto;
import com.alibou.security.about.dto.AboutRuDto;
import com.alibou.security.about.dto.AboutUzDto;
import com.alibou.security.about.entity.About;
import com.alibou.security.exception.ResourceNotFoundException;
import com.alibou.security.exception.ValidationException;
import jakarta.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
@Transactional
public class AboutService {
    private final AboutRepository aboutRepository;

    public List<AboutUzDto> getAboutUz() {
        List<About> abouts = aboutRepository.findAll();
        return abouts.stream().map(item -> new AboutUzDto(item.getId(), item.getDescription())).toList();
    }

    public List<AboutRuDto> getAboutRu() {
        List<About> abouts = aboutRepository.findAll();
        return abouts.stream().map(item -> new AboutRuDto(item.getId(), item.getDescriptionRu())).toList();
    }

    public List<AboutEnDto> getAboutEn() {
        List<About> abouts = aboutRepository.findAll();
        return abouts.stream().map(item -> new AboutEnDto(item.getId(), item.getDescriptionEn())).toList();
    }

    public AboutCreateDto createAbout(AboutCreateDto aboutCreateDto) {
        if (aboutCreateDto == null) {
            throw new ValidationException("Description cannot be null");
        }
        if (aboutCreateDto.getDescription().isBlank() || aboutCreateDto.getDescriptionRu().isBlank() || aboutCreateDto.getDescriptionEn().isBlank()) {
            throw new ValidationException("Description cannot be blank");
        }
        About about = new About(UUID.randomUUID(), aboutCreateDto.getDescription(), aboutCreateDto.getDescriptionRu(), aboutCreateDto.getDescriptionEn());
        About saved = aboutRepository.save(about);
        return new AboutCreateDto(saved.getDescription(), saved.getDescriptionRu(), saved.getDescriptionEn());
    }

    public About updateAbout(AboutCreateDto aboutCreateDto, UUID id) {
        About about = aboutRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Could not find " + id));

        about.setDescription(aboutCreateDto.getDescription());
        about.setDescriptionRu(aboutCreateDto.getDescriptionRu());
        about.setDescriptionEn(aboutCreateDto.getDescriptionEn());

        return aboutRepository.save(about);
    }

    public Boolean delete(UUID id) {
        aboutRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Could not find " + id));
        aboutRepository.deleteById(id);
        return true;
    }

    public About getAbout(UUID id) {
        return aboutRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Could not find " + id));
    }
}
